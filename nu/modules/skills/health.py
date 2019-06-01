# Dock to recharge on low battery

from ast import literal_eval
from random import SystemRandom
from distutils.util import strtobool
from nu.modules.body.executor import ExecutableActions, ExecutableSingleEmotes, ExecutableChainEmotes
from nu.modules.body import senses
from nu.modules.skill import Skill
from nu.modules.config import skill_config

config = skill_config()


class Health:

    SUBSCRIPTIONS = ['BodySenseBattery', 'BodySenseRecharging']
    PRIORITY = int(config.get('HealthSkill', 'priority'))
    EXPIRATION = int(config.get('HealthSkill', 'expiration'))
    LOW_VOLTAGE = float(config.get('HealthSkill', 'low'))
    HIGH_VOLTAGE = float(config.get('HealthSkill', 'high'))

    def __init__(self):
        self.voltage = __class__.LOW_VOLTAGE
        self.recharging = False
        self.charger = True
        self.attempts = 0

    def battery_is_low(self):
        return self.voltage <= __class__.LOW_VOLTAGE

    def battery_is_high(self):
        return self.voltage >= __class__.HIGH_VOLTAGE

    def handle_message(self, message):
        channel = message.get('channel').decode()
        if channel == senses.BodySenseBattery.id():
            self.voltage = float(message.get('data').decode())
        elif channel == senses.BodySenseRecharging.id():
            data = literal_eval(message.get('data').decode('utf-8'))
            self.recharging = data.get('charging')
            self.charger = data.get('on_charger')

        if self.recharging:
            if self.battery_is_high():
                self.attempts = 0
                payload = Skill.payload()
                payload.append(Skill.message(ExecutableActions.UNDOCK_FROM_CHARGER))
                payload.append(Skill.message(ExecutableActions.BECOME_IDLE))
                Skill.enqueue(__class__, payload, )
            else:
                payload = Skill.payload()
                payload.append(Skill.message(ExecutableActions.BECOME_ASLEEP))
                Skill.enqueue(__class__, payload)

        if self.recharging == False:
            if self.battery_is_low():
                self.attempts += 1
                payload = Skill.payload()
                if self.attempts <= 2:
                    text = SystemRandom().choice([
                        "I'm tired...",
                        "I'm not feeling well...",
                        "I'm feeling weak..."
                    ])
                    payload.append(Skill.message(ExecutableActions.EMOTE_SINGLE, {'type': ExecutableSingleEmotes.UNHAPPY}))
                    payload.append(Skill.message(ExecutableActions.SPEAK_SLOW, {'text': text}, sleep=10))
                else:
                    text = SystemRandom().choice([
                        "Where's my charger?",
                        "I need to recharge.",
                        "I want my charger!",
                        "Is my docking station around?"
                    ])
                    payload.append(Skill.message(ExecutableActions.SPEAK_FAST, {'text': text}))
                    payload.append(Skill.message(ExecutableActions.EMOTE_SINGLE, {'type': ExecutableSingleEmotes.TIRED}))
                payload.append(Skill.message(ExecutableActions.DOCK_AND_RECHARGE, sleep=25))
                Skill.enqueue(__class__, payload)
            elif self.charger:
                payload = Skill.payload()
                payload.append(Skill.message(ExecutableActions.MOVE_FORWARD, {'distance': 4}))
                payload.append(Skill.message(ExecutableActions.BECOME_IDLE))
                Skill.enqueue(__class__, payload)

    def handle_failure(self, action, params):
        payload = Skill.payload()
        payload.append(Skill.message(ExecutableActions.EMOTE_SINGLE, {'type': ExecutableSingleEmotes.UPSET}))
        Skill.enqueue(__class__, payload)

    def handle_success(self, action, params):
        if self.recharging == False:
            payload = Skill.payload()
            payload.append(Skill.message(ExecutableActions.EMOTE_CHAIN, {'type': ExecutableChainEmotes.FALL_ASLEEP}))
            payload.append(Skill.message(ExecutableActions.BECOME_ASLEEP))
            Skill.enqueue(__class__, payload)


HealthSkill = Health()