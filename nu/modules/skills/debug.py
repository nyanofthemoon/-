# Being Touched

import logging
from ast import literal_eval
from distutils.util import strtobool

from nu.modules.body.executor import ExecutableActions
from nu.modules.skill import Skill
from nu.modules.body import senses
from nu.modules.config import skill_config

logger = logging.getLogger()
config = skill_config()


class Debug:

    SUBSCRIPTIONS = ['BodySenseAirborne', 'BodySenseTouch', 'BodySenseCalm', 'BodySenseCharging', 'BodySenseCliff', 'BodySenseCubeBatteryLow', 'BodySenseRobotBatteryLow', 'BodySenseUserIntent', 'BodySenseWakeWord']
    PRIORITY = int(config.get('DebugSkill', 'priority'))
    EXPIRATION = int(config.get('DebugSkill', 'expiration'))

    #def __init__(self):
    #    self.test = 1

    def handle_message(self, message):
        channel = message.get('channel').decode()
        data = str(literal_eval(message.get('data').decode('utf-8'))).lower()
        if channel == senses.BodySenseTouch.id():
            if True == strtobool(data):
                logger.debug('Touched!')
        elif channel == senses.BodySenseAirborne.id():
            if True == strtobool(data):
                logger.debug('Airborne!')
        elif channel == senses.BodySenseCalm.id():
            if True == strtobool(data):
                logger.debug('Resting...')
        elif channel == senses.BodySenseCharging.id():
            if True == strtobool(data):
                logger.debug('Charging...')
        elif channel == senses.BodySenseCliff.id():
            if True == strtobool(data):
                logger.debug('There is a cliff.')
        elif channel == senses.BodySenseCubeBatteryLow.id():
            if True == strtobool(data):
                logger.debug('Cube battery is low.')
        elif channel == senses.BodySenseRobotBatteryLow.id():
            if True == strtobool(data):
                logger.debug('Robot battery is low.')
        elif channel == senses.BodySenseFalling.id():
            if True == strtobool(data):
                logger.debug('Falling!!!')
        elif channel == senses.BodySenseUserIntent.id():
            logger.debug('Internal user_intent Event detected.')
        elif channel == senses.BodySenseWakeWord.id():
            logger.debug('Internal wake_word Event detected.')
        else:
            return False

    def handle_failure(self, action, params):
        return None

    def handle_success(self, action, params):
        return None


DebugSkill = Debug()