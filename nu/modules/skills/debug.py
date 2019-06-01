# Being Touched

from ast import literal_eval
from distutils.util import strtobool

from nu.modules.body.executor import ExecutableActions
from nu.modules.skill import Skill
from nu.modules.body import senses
from nu.modules.config import skill_config

config = skill_config()


class Debug:

    SUBSCRIPTIONS = ['BodySenseAirborne', 'BodySenseTouch', 'BodySenseCharging', 'BodySenseCliff', 'BodySenseCubeBatteryLow', 'BodySenseRobotBatteryLow']
    PRIORITY = int(config.get('DebugSkill', 'priority'))
    EXPIRATION = int(config.get('DebugSkill', 'expiration'))

    #def __init__(self):
    #    self.voltage = __class__.LOW_VOLTAGE
    #    self.recharging = False

    def handle_message(self, message):
        channel = message.get('channel').decode()
        data = literal_eval(message.get('data').decode('utf-8'))
        payload = Skill.payload()
        if channel == senses.BodySenseTouch.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'Touch'}))
        elif channel == senses.BodySenseAirborne.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'Airborne'}))
        elif channel == senses.BodySenseCharging.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'Charging'}))
        elif channel == senses.BodySenseCliff.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'There is a cliff!'}))
        elif channel == senses.BodySenseCubeBatteryLow.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'Cube battery is low'}))
        elif channel == senses.BodySenseRobotBatteryLow.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'Robot battery is low'}))
        elif channel == senses.BodySenseFalling.id():
            if True == strtobool(data):
                payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': 'Falling'}))
        else:
            payload.append(Skill.message(ExecutableActions.SPEAK_SLOW, {'text': 'Nothing to say for channel ' + channel}))
        Skill.enqueue(__class__, payload)

    def handle_failure(self, action, params):
        return None

    def handle_success(self, action, params):
        return None


DebugSkill = Debug()