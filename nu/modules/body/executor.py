# Interface to robot

import time
import asyncio
import logging
from nu import anki_vector
from nu.anki_vector.util import degrees, distance_inches, speed_mmps, radians
from anki_vector.connection import ControlPriorityLevel
from random import SystemRandom, randint

logger = logging.getLogger()


class Executor:

    def __init__(self, robot: anki_vector.robot.AsyncRobot):
        self.robot = robot

    def reset(self):
        self.constitution = 1
        self.energy = 1
        self.happy = 1

    async def is_robot_battery_low(self):
        battery_state = await asyncio.wrap_future(self.robot.get_battery_state())
        return battery_state.battery_level == 1

    async def is_cube_battery_low(self):
        battery_state = await asyncio.wrap_future(self.robot.get_battery_state())
        return battery_state.cube_battery.level == 1

    async def is_robot_on_charger(self):
        return self.robot.status.is_on_charger

    async def is_robot_charging(self):
        return self.robot.status.is_charging

    async def is_robot_wheels_moving(self):
        return self.robot.status.are_wheels_moving

    async def is_robot_playing_animation(self):
        return self.robot.status.is_animating

    # In someone's hand ; is_robot_stable_to_move will also return False
    async def is_robot_being_held(self):
        return self.robot.status.is_being_held

    # Not in a stable state with threads down
    async def is_robot_stable_enough_to_move(self):
        return not self.robot.status.is_picked_up

    async def is_robot_button_pressed(self):
        return self.robot.status.is_button_pressed

    async def is_robot_carrying_cube(self):
        return self.robot.status.is_carrying_block

    async def has_robot_detected_cliff(self):
        return self.robot.status.is_cliff_detected

    # Docking with cube or charger, etc
    async def is_robot_docking(self):
        return self.robot.status.is_docking_to_marker

    async def is_robot_falling(self):
        return self.robot.status.is_falling

    async def is_robot_moving_head(self):
        return not self.robot.status.is_head_in_pos

    async def is_robot_moving_lift(self):
        return not self.robot.status.is_lift_in_pos

    # Moving to a locationg
    async def is_robot_pathing(self):
        return self.robot.status.is_pathing

    # Sleeping or charging
    async def is_robot_calm(self):
        return self.robot.status.is_in_calm_power_mode

    # Any motors moving
    async def is_robot_moving(self):
        return self.robot.status.is_robot_moving

    async def get_robot_last_touch_data(self):
        return self.robot.touch.last_sensor_reading

    async def is_robot_being_touched(self):
        touch_data = await self.get_robot_last_touch_data()
        if touch_data is not None:
            return touch_data.is_being_touched
        return False

    async def get_robot_charger(self):
        return self.robot.world.charger

    async def connect_cube(self):
        return self.robot.world.connect_cube()

    async def disconnect_cube(self):
        return self.robot.world.disconnect_cube()

    async def flash_cube_lights(self):
        return self.robot.world.flash_cube_lights()

    async def drive_on_charger(self):
        if self.is_robot_on_charger() == False:
            return self.robot.behavior.drive_on_charger()
        return asyncio.sleep(0.5)

    async def drive_off_charger(self):
        if self.is_robot_on_charger() == True:
           return self.robot.behavior.drive_off_charger()
        return asyncio.sleep(0.5)

    async def speak_slowly(self, text):
        return self.robot.behavior.say_text(text, 0.5)

    async def speak(self, text):
        return self.robot.behavior.say_text(text)

    async def speak_fast(self, text):
        return self.robot.behavior.say_text(text, 1.5)

    async def set_eye_color(self, hue, saturation):
        return self.robot.behavior.set_eye_color(hue, saturation)

    async def go_forward(self, inches=1.0, mmps=1.0):
        return self.robot.behavior.drive_straight(distance_inches(inches), speed_mmps(mmps))

    async def go_backwards(self, inches=1.0, mmps=1.0):
        return self.robot.behavior.drive_straight(distance_inches(inches*-1), speed_mmps(mmps))

    async def turn(self, angle):
        return self.robot.behavior.turn_in_place(degrees(angle))

    async def turn_right(self):
        return self.turn(-90)

    async def turn_left(self):
        return self.turn(90)

    async def turn_around(self):
        return self.turn(180)

    async def set_head_angle(self, angle):
        return self.robot.behavior.set_head_angle(degrees(angle))

    async def set_lift_height(self, height):
        return self.robot.behavior.set_lift_height(height)

    async def request_control(self):
        if self.robot.conn._has_control == False:
            return self.robot.conn.request_control(ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
        return asyncio.sleep(0.5)

    async def release_control(self):
        if self.robot.conn._has_control == True:
            return self.robot.conn.release_control()
        return asyncio.sleep(0.5)


class ExecutableActions:
    SPEAK_SLOW = 'speak_slowly'
    SPEAK = 'speak'
    SPEAK_FAST = 'speak_fast'
    FLASH_CUBE_LIGHTS = 'flash_cube_lights'
    DRIVE_ON_CHARGER = 'drive_on_charger'
    DRIVE_OFF_CHARGER = 'drive_off_charger'
    SET_EYE_COLOR = 'set_eye_color'
    GO_FORWARD = 'go_forward'
    GO_BACKWARD = 'go_backwards'
    TURN_RIGHT = 'turn_right'
    TURN_LEFT = 'turn_left'
    SET_HEAD_ANGLE = 'set_head_angle'
    SET_LIFT_HEIGHT = 'set_lift_height'
