# Raspberry Pi machinecontrol interface
 
## Initialise the machine control card

    machine = machinecontrol()

## TWO-WAY MOTOR OUTPUTS
> Valid output values are: OFF, LEFT, RIGHT, UP, DOWN

    # Assign a machine two-way motor output to a variable (range 1..7)
    nicemotorname = machine.twowaymotor[4]
    # Set a two-way motor output direction (using variable)
    nicemotorname.direction = machinecontrol.UP
    # Set a two-way motor output direction (directly)
    machine.twowaymotor[3] = machinecontrol.RIGHT

## POWER (220V) OUTPUTS
> Valid output values are: ON, OFF

    # Assign a power output to a variable (range 1..2)
    nicepowername = machine.power[2]
    # Set a power output (using variable)
    nicepowername.value = machinecontrol.ON
    # Set a power output (directly)
    machine.power[1] = machinecontrol.ON

## STANDARD MOTOR OUTPUTS
> Valid output values are: ON, OFF

    # Assign a standard motor output to a variable (range 1..3)
    nicemotornamestd = machine.motor[2]
    # Set a standard motor output (using variable)
    nicemotornamestd.value = machinecontrol.ON
    # Set a standard motor output (directly)
    machine.motor[3] = machinecontrol.ON

## STANDARD DIGITAL INPUTS / OUTPUTS
### INFO
> Input pins have a pull-up resistor and
> will return True if not connected
> All I/O is configured as INPUTS at
> system boot

### !WARNING!
> Setting an output to OFF and supplying 
> a voltage (VCC) to the output pin will
> damage the interface card

> Valid output values are: ON, OFF

    # Read an input (range 0..31)
    print('I4:', machine.input[4])
    # Set an output (range 0..31)
    machine.output[19] = machinecontrol.OFF

## TEMPERATURE INPUT
> Return value in °C

    # Read temperature (DB18B20 sensor)
    print('T:', machine.temperature, '°C')
