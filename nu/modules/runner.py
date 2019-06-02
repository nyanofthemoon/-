# Runner

import asyncio
import logging
import threading
from distutils.util import strtobool
from time import sleep
from nu import anki_vector
from anki_vector.events import Events
from anki_vector.user_intent import UserIntent, UserIntentEvent

from .scheduler import Scheduler
from .body import Executor
from .body.senses import *
from .brain import SMemoryQueue, SMemoryPubSub, SMemoryStorage
from .brain import LMemory
from .brain import Operator
from .brain.senses import *
from .config import nu_config
from .config import runner_config
from .config import sense_config
from .config import skill_config
from .skills import *


nuConfig = nu_config()
runnerConfig = runner_config()
senseConfig = sense_config()
skillConfig = skill_config()


class Runner:

    smemory = None
    lmemory = None
    operator = None
    executor = None
    scheduler = None
    schedulerThread = None
    pubsubThread = None

    def __init__(self):
        self.recognizer = None
        self.audioData = None
        self.scheduler = Scheduler()

    async def scheduleTasks(self, sensors=[], exclusions=[]):
        for sensor in sensors:
            if sensor not in exclusions:
              self.scheduler.add(int(senseConfig.get('refresh', sensor)), getattr(globals()[sensor], 'publish'))

    def startScheduledTasks(self):
        self.schedulerThread = threading.Thread(daemon=True, target=self.scheduler.start)
        self.schedulerThread.start()
        self.schedulerThread.join()

    def stopScheduledTasks(self):
        self.scheduler.stop()
        self.schedulerThread._stop()

    def startShortTermMemory(self):
        SMemoryStorage.flushdb()
        SMemoryQueue.flush()
        SMemoryQueue.start(self.operator.handle_entry)

    def stopShortTermMemory(self):
        SMemoryQueue.stop()

    def startLongTermMemory(self):
        self.lmemory = LMemory()

    def stopLongTermMemory(self):
        return True

    async def _sensorCallbackBodySenseAirborne(self):
        is_airborne = not await self.executor.is_robot_stable_enough_to_move()
        if is_airborne == True:
          BodySenseAirborne.publish(True)
    async def _sensorCallbackBodySenseButtonPressed(self):
        is_robot_button_pressed = await self.executor.is_robot_button_pressed()
        if is_robot_button_pressed == True:
            BodySenseButtonPress.publish(True)
    async def _sensorCallbackBodySenseCalm(self):
        is_robot_calm = await self.executor.is_robot_calm()
        if is_robot_calm == True:
            BodySenseCalm.publish(True)
    async def _sensorCallbackBodySenseCharging(self):
        is_robot_charging = await self.executor.is_robot_charging()
        if is_robot_charging == True:
            BodySenseCharging.publish(True)
    async def _sensorCallbackBodySenseCliff(self):
        has_robot_detected_cliff = await self.executor.has_robot_detected_cliff()
        if has_robot_detected_cliff == True:
            BodySenseCliff.publish(True)
    async def _sensorCallbackBodySenseCubeBatteryLow(self):
        is_cube_battery_low = await self.executor.is_cube_battery_low()
        if is_cube_battery_low == True:
            BodySenseCubeBatteryLow.publish(True)
    async def _sensorCallbackBodySenseRobotBatteryLow(self):
        is_robot_battery_low = await self.executor.is_robot_battery_low()
        if is_robot_battery_low == True:
            BodySenseRobotBatteryLow.publish(True)
    async def _sensorCallbackBodySenseTouch(self):
        is_being_touched = await self.executor.is_robot_being_touched()
        if is_being_touched == True:
            BodySenseTouch.publish(True)
    async def _sensorCallbackBodySenseFalling(self):
        is_robot_falling = await self.executor.is_robot_falling()
        if is_robot_falling == True:
            BodySenseFalling.publish(True)

    async def bindSensoryCallback(self, robot: anki_vector.robot.AsyncRobot, sensors):
        sensoryEvent = threading.Event()
        if 'BodySenseAirborne' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseAirborne')), self._sensorCallbackBodySenseAirborne)
        if 'BodySenseButtonPress' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseButtonPress')), self._sensorCallbackBodySenseButtonPressed)
        if 'BodySenseCalm' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseCalm')), self._sensorCallbackBodySenseCalm)
        if 'BodySenseCliff' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseCliff')), self._sensorCallbackBodySenseCliff)
        if 'BodySenseCharging' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseCharging')), self._sensorCallbackBodySenseCharging)
        if 'BodySenseCubeBatteryLow' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseCubeBatteryLow')), self._sensorCallbackBodySenseCubeBatteryLow)
        if 'BodySenseFalling' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseFalling')), self._sensorCallbackBodySenseFalling)
        if 'BodySenseRobotBatteryLow' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseRobotBatteryLow')), self._sensorCallbackBodySenseRobotBatteryLow)
        if 'BodySenseTouch' in sensors:
            self.scheduler.add(int(senseConfig.get('refresh', 'BodySenseTouch')), self._sensorCallbackBodySenseTouch)
        if 'BodySenseUserIntent' in sensors:
            robot.events.subscribe(sensorCallbackBodySenseUserIntent, Events.user_intent, sensoryEvent)
        if 'BodySenseWakeWord' in sensors:
            robot.events.subscribe(sensorCallbackBodySenseWakeWord, Events.user_intent, sensoryEvent)

    def unbindSensoryCallback(self):
        self.scheduler.empty()
        return True

    def bindMessageCallback(self, skills):
        for skill in skills:
            skillClass = globals()[skill]
            for subscription in getattr(skillClass, 'SUBSCRIPTIONS'):
                sensorClass = globals()[subscription]
                sensorClass.subscribe(skillClass.handle_message)

        self.pubsubThread = SMemoryPubSub.run_in_thread(sleep_time=0.5, daemon=True)

    def unbindMessageCallback(self):
        SMemoryPubSub.punsubscribe('*')
        self.pubsubThread.stop()

    def startLogicalOperator(self):
        self.operator = Operator(self.executor)

    def stopLogicalOperator(self):
        self.operator = None
        return True

    def startPhysicalExecutor(self, robot: anki_vector.robot.AsyncRobot):
        self.executor = Executor(robot)
        self.executor.reset()
        return True

    def stopPhysicalExecutor(self):
        self.executor = None
        return True

logger = logging.getLogger()
runner = None

async def main_function():
    global runner
    runner = Runner()
    await run_vector_program()

async def run_vector_program():
    logger.info('Contacting Vector SDK')
    try:
        config = {
            "name": nuConfig.get('sdk', 'name'),
            "guid": nuConfig.get('sdk', 'guid'),
            "cert": nuConfig.get('sdk', 'cert')
        }
        showVisionViewer = strtobool(runnerConfig.get('options', 'ShowVision'))
        showNavigationViewer = strtobool(runnerConfig.get('options', 'ShowNavigationMap'))

        robot = anki_vector.AsyncRobot(
            serial=nuConfig.get('sdk', 'serial'),
            ip=nuConfig.get('sdk', 'ip'),
            config=config,
            default_logging=False,
            cache_animation_lists=False,
            behavior_activation_timeout=int(runnerConfig.get('options', 'BehaviorActivationTimeout')),
            enable_face_detection=True,
            estimate_facial_expression=True,
            enable_audio_feed=True,
            enable_custom_object_detection=True,
            enable_nav_map_feed=False,
            show_viewer=showVisionViewer,
            show_3d_viewer=showNavigationViewer,
        )
        robot.connect()
        await vector_connect_callback(robot)

    except anki_vector.exceptions.VectorConnectionException as e:
        logger.critical('Vector SDK Connection Timeout')
        robot.disconnect()
        sleep(1.5)
        run_vector_program()

    except SystemExit as e:
        logger.critical('Vector System Error')
        robot.disconnect()
        sleep(1.5)
        run_vector_program()

async def vector_connect_callback(robot: anki_vector.robot.AsyncRobot):
    global runner

    skills = []
    for name, status in skillConfig.items('status'):
        if strtobool(status):
            skills.append(name)

    sensors = []
    ex_sensors = [
        'BodySenseAirborne',
        'BodySenseCalm',
        'BodySenseCharging',
        'BodySenseCliff',
        'BodySenseCubeBatteryLow',
        'BodySenseRobotBatteryLow',
        'BodySenseTouch',
        'BodySenseFalling',
        'BodySenseUserIntent',
        'BodySenseWakeWord',
    ]

    for skill in skills:
        for sensor in getattr(globals()[skill], 'SUBSCRIPTIONS'):
            if sensor not in sensors:
                sensors.append(sensor)

    logger.info('Connected to Vector SDK')
    logger.info('Contacting Long Term Memory')
    runner.startLongTermMemory()
    logger.info('Starting Physical Executor')
    runner.startPhysicalExecutor(robot)
    logger.info('Starting Logical Operator')
    runner.startLogicalOperator()
    logger.info('Contacting Short Term Memory')
    runner.startShortTermMemory()
    logger.info('Finding Required Sensors ' + str(sensors))
    logger.info('Excluding Sensors ' + str(ex_sensors))
    await runner.bindSensoryCallback(robot, sensors)
    runner.bindMessageCallback(skills)
    logger.info('Initializing Skills ' + str(skills))
    await runner.scheduleTasks(sensors, ex_sensors)
    runner.startScheduledTasks()


def vector_disconnect_callback():
    global runner
    logger.critical('Disconnected from Vector SDK')
    logger.warning('Unscheduling Recurrent Tasks')
    runner.stopScheduledTasks()
    logger.warning('Disconnecting from Sensors')
    runner.unbindSensoryCallback()
    runner.unbindMessageCallback()
    logger.warning('Forgetting Short Term Memory')
    runner.stopShortTermMemory()
    logger.warning('Stopping Logical Operator')
    runner.stopLogicalOperator()
    logger.warning('Stopping Physical Executor')
    runner.stopPhysicalExecutor()
    run_vector_program()


def sensorCallbackBodySenseUserIntent(robot, event_type, event, evt):
    BodySenseUserIntent.publish(str(event))
    evt.set()

def sensorCallbackBodySenseWakeWord(robot, event_type, event, evt):
    BodySenseWakeWord.publish(str(event))
    evt.set()