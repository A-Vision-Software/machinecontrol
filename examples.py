#/*******************************************************************************
#*
#* (c) 2022 Copyright A-Vision Software
#*
#* File description :        Python machine control examples
#*
#* Created by       :        Arnold Velzel
#* Created on       :        17-05-2022
#*
#*******************************************************************************/

from time import sleep
from avisionmachinecontrol import machinecontrol

# Initialise the machine control card
machine = machinecontrol()

#############################
### TWO-WAY MOTOR OUTPUTS ###
#############################
#
# Valid output values are:
#   OFF, LEFT, RIGHT, UP, DOWN
#
#############################
print('TWO-WAY MOTOR OUTPUTS')
# Assign a machine two-way motor output to a variable (range 1..7)
nicemotorname = machine.twowaymotor[4]
# Set a two-way motor output direction (using variable)
nicemotorname.direction = machinecontrol.UP
# Set motor speed (PWM)
nicemotorname.speed = 0.8
# Set a two-way motor output direction (directly)
machine.twowaymotor[3] = machinecontrol.RIGHT
machine.twowaymotor[3].speed = 0.2

sleep(5)

# Update motor speed (PWM)
nicemotorname.speed = 0.1

sleep(5)

# Set a two-way motor output direction (using variable)
nicemotorname.direction = machinecontrol.DOWN
# Update motor speed (PWM)
nicemotorname.speed = 0.3
# Set a two-way motor output direction (directly)
machine.twowaymotor[3] = machinecontrol.LEFT

sleep(5)

nicemotorname.direction = machinecontrol.OFF
machine.twowaymotor[3] = machinecontrol.OFF

sleep(1)

############################
### POWER (220V) OUTPUTS ###
############################
#
# Valid output values are:
#   ON, OFF
#
############################
print('POWER (220V) OUTPUTS')
# Assign a power output to a variable (range 1..2)
nicepowername = machine.power[2]
# Set a power output (using variable)
nicepowername.value = machinecontrol.ON
# Set a power output (directly)
machine.power[1] = machinecontrol.ON

sleep(1)

##############################
### STANDARD MOTOR OUTPUTS ###
##############################
#
# Valid output values are:
#   ON, OFF
#
##############################
print('STANDARD MOTOR OUTPUTS')
# Assign a standard motor output to a variable (range 1..3)
nicemotornamestd = machine.motor[2]
# Set a standard motor output (using variable)
nicemotornamestd.value = machinecontrol.ON
# Set a standard motor output (directly)
machine.motor[3] = machinecontrol.ON

sleep(1)

#########################################
### STANDARD DIGITAL INPUTS / OUTPUTS ###
#########################################
#
# INFO
#  Input pins have a pull-up resistor and
#  will return True if not connected
#  All I/O is configured as INPUTS at
#  system boot
#
# !WARNING!
#  Setting an output to OFF and supplying 
#  a voltage (VCC) to the output pin will
#  damage the interface card
#
# Valid output values are:
#   ON, OFF
#
#########################################
print('STANDARD DIGITAL INPUTS / OUTPUTS')
# Read an input (range 0..31)
print('I4:', machine.input[4])
# Set an output (range 0..31)
machine.output[19] = machinecontrol.OFF

sleep(1)

#########################
### TEMPERATURE INPUT ###
#########################
#
# Return value in °C
#
#########################
print('TEMPERATURE INPUT')
# Read temperature (DB18B20 sensor)
print('T:', machine.temperature, '°C')

sleep(1)
