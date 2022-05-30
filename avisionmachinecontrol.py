#/*******************************************************************************
#*
#* File description :       A-Vision Solutions machine control card module
#*
#* Created by       :       Arnold Velzel
#* Created on       :       04-04-2022
#*
#* Required         :       pcf8575, gpiozero
#*
#* sudo apt update
#* sudo apt upgrade
#* sudo apt autoremove
#* sudo apt-get install libffi-dev
#* sudo apt-get install python3-pip
#* sudo pip3 install smbus2
#* sudo pip3 install w1thermsensor (https://github.com/timofurrer/w1thermsensor)
#*
#* sudo raspi-config
#*  -> Interface Options
#*    -> Enable I2C support
#*    -> Enable 1-Wire support
#*
#*******************************************************************************/

from gpiozero import Motor, LED
from time import sleep

from pcf8575 import PCF8575
from w1thermsensor import W1ThermSensor

# Constants for easy programming
class machineconstants:
    OFF = 0
    ON = 1
    LEFT = 1
    RIGHT = 2
    UP = 1
    DOWN = 2
    BREAK = 3

# All power outputs as a list
class machinecontrolpower(list):

    def __init__(self, machinecontrol, *args, **kwargs):
        super(machinecontrolpower, self).__init__(*args, **kwargs)
        self.machinecontrol = machinecontrol

    def __setitem__(self, key, value):
        assert key <= len(self)
        self.machinecontrol._set_power_output(key, value)

    def __getitem__(self, key):
        assert key <= len(self)
        return self.machinecontrol._P[key]

    def __len__(self):
        return 2

# All additional (PCF) inputs/outputs as a list
class machinecontrolport(list):

    def __init__(self, machinecontrol, *args, **kwargs):
        super(machinecontrolport, self).__init__(*args, **kwargs)
        self.machinecontrol = machinecontrol

    def __setitem__(self, key, value):
        assert key < len(self)
        self.machinecontrol._set_output(key, value)

    def __getitem__(self, key):
        assert key < len(self)
        return self.machinecontrol._get_input(key)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return 32

# All standard motor control outputs as a list
class machinecontrolmotor(list):

    def __init__(self, machinecontrol, *args, **kwargs):
        super(machinecontrolmotor, self).__init__(*args, **kwargs)
        self.machinecontrol = machinecontrol

    def __setitem__(self, key, value):
        assert key <= len(self)
        self.machinecontrol._set_motor_output(key, value)

    def __getitem__(self, key):
        assert key <= len(self)
        return self.machinecontrol._OUT[key]

    def __len__(self):
        return 3

# All two-way motor control outputs as a list
class machinecontroltwowaymotor(list):

    def __init__(self, machinecontrol, *args, **kwargs):
        super(machinecontroltwowaymotor, self).__init__(*args, **kwargs)
        self.machinecontrol = machinecontrol

    def __setitem__(self, key, value):
        assert key <= len(self)
        self.machinecontrol._set_twowaymotor_output(key, value)

    def __getitem__(self, key):
        assert key <= len(self)
        return self.machinecontrol._M[key]

    def __len__(self):
        return 7

# A single two-way motor control class
class twowaymotor:

    def __init__(self, pinLeft, pinRight):
        self.motor = Motor(pinLeft, pinRight)
        #self.pinLeft = LED(pinLeft)
        #self.pinRight = LED(pinRight)
        self._speed = 1
        self._direction = machineconstants.OFF
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        assert value <= 1
        self._speed = value
        self.direction = self._direction

    @property
    def direction(self):
        return None
    
    @direction.setter
    def direction(self, value):
        if (value == machineconstants.OFF and self._direction != machineconstants.OFF):
            self.motor.stop()

        if (value == machineconstants.LEFT and self._direction != machineconstants.LEFT):
            if (self._direction != machineconstants.OFF or self.motor.is_active):
                self.motor.stop()
                sleep(0.01)

            self.motor.forward(self._speed)

        if (value == machineconstants.LEFT and self._direction == machineconstants.LEFT):
            self.motor.forward(self._speed)

        if (value == machineconstants.RIGHT and self._direction != machineconstants.RIGHT):
            if (self._direction != machineconstants.OFF or self.motor.is_active):
                self.motor.stop()
                sleep(0.01)

            self.motor.backward(self._speed)

        if (value == machineconstants.RIGHT and self._direction == machineconstants.RIGHT):
            self.motor.backward(self._speed)

        if (value == machineconstants.BREAK and self._direction != machineconstants.BREAK):
            self.motor.backward(0)

        self._direction = value

# The machine control class
class machinecontrol(machineconstants):

    def __init__(self):
        self._PCF1 = PCF8575(1, 0x20)
        self._PCF2 = PCF8575(1, 0x21)

        self._OUT = [None, LED(13), LED(12), LED(6)]
        self._M = [None, twowaymotor(11, 8), twowaymotor(25, 10), twowaymotor(16, 26), twowaymotor(23, 24), twowaymotor(19, 18), twowaymotor(9, 7), twowaymotor(22, 5)]
        self._P = [None, LED(27), LED(17)]

    @property
    def temperature(self):
        try:
            DS18B20 = W1ThermSensor()
            return DS18B20.get_temperature()
        except:
            return None
    
    @property
    def power(self):
        return machinecontrolpower(self)

    @property
    def output(self):
        return machinecontrolport(self)

    @property
    def input(self):
        return machinecontrolport(self)

    @property
    def motor(self):
        return machinecontrolmotor(self)

    @property
    def twowaymotor(self):
        return machinecontroltwowaymotor(self)

    def _set_power_output(self, num, value):
        if (value == self.ON):
            value = True
        if (value == self.OFF):
            value = False
        if (1 <= num <= 2):
            if (value):
                self._P[num].on()
            else:
                self._P[num].off()

    def _set_output(self, num, value):
        if (value == self.ON):
            value = True
        if (value == self.OFF):
            value = False
        if (num <= 15):
            self._PCF1.port[num] = value
        if (num > 15):
            self._PCF2.port[num - 16] = value

    def _get_input(self, num):
        if (num <= 15):
            self._PCF1.port[num] = True # initialise as INPUT
            return self._PCF1.port[num]
        if (num > 15):
            self._PCF2.port[num - 16] = True # initialise as INPUT
            return self._PCF2.port[num - 16]
        return None

    def _set_motor_output(self, num, value):
        if (value == self.ON):
            value = True
        if (value == self.OFF):
            value = False
        if (1 <= num <= 3):
            if (value):
                self._OUT[num].on()
            else:
                self._OUT[num].off()

    def _set_twowaymotor_output(self, num, value):
        if (1 <= num <= 7):
            self._M[num].direction = value

