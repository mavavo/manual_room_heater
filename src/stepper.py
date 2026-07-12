from machine import Pin
from time import sleep_us

# pins on pico:
STEP_PIN = 17  # assigned physical pin: 22
DIR_PIN = 16   # assigned physical pin: 21
EN_PIN = 20    # ENABLE pin, assigned physical pin: 26

en_pin = Pin(EN_PIN, Pin.OUT, value=1)   # value = 1 means driver disables motor (requires connection of ENABLE pin at driver and one GPIO at Pico), 0 means always enabled
dir_pin = Pin(DIR_PIN, Pin.OUT, value=0)
step_pin = Pin(STEP_PIN, Pin.OUT, value=0)

def enable(state=True):
    en_pin.value(0 if state else 1)

def set_direction(clockwise=True):
    dir_pin.value(1 if clockwise else 0)
    sleep_us(5)  # > 650 ns setup time needed

def step_once(pulse_us=10, pause_us=10):
    step_pin.on()
    sleep_us(pulse_us)   # signal on 1 for at least 1.9 µs at the step pin 
    step_pin.off()
    sleep_us(pause_us)   # signal on 0 for at least 1.9 µs at the step pin

def move_steps(steps, speed_sps=200, clockwise=True):
    'Moves the motor in the given direction by the given number of stepts'
    if steps <= 0:
        return

    set_direction(clockwise)

    if speed_sps <= 0:
        speed_sps = 100

    full_period = (1/speed_sps) * 10**6         # µs/step
    half_period = int(full_period/2)            # µs/half_step
    if half_period < 5:   # avoid pulses below 1.9 µs plus some buffer
        half_period = 5  

    enable(True)
    sleep_us(500)

    try:
        for _ in range(steps):
            step_once(half_period, half_period)
    finally:
        step_pin.off()
        enable(False)
        sleep_us(500)