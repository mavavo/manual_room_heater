from stepper import move_steps
import time
from time import localtime, sleep
from wlan import sync_times_via_ntp, disconnect_wlan, wlan


UTC_OFFSET = 1  # UTC offset winter
sync_times_via_ntp()

def now() -> tuple:
    'Returns the local, current time with respect to the UTC as an 8 tuple (year, month, day, hour, minute, second, weekday, yearday)'
    return localtime(time.time() + UTC_OFFSET * 3600)

def main():
    'Moves the motor at the time set, keeps it at this position for the heating time and then moves back to origin'
    steps_to_move = 3200  # runs on 1/8 step increment, 720° revolution at the motor results in round about 90° revolution at the wheel
    heating_time = 1     # in minutes
    while True:
        current_time = now()
        if current_time[3] == 8 and current_time[4] == 30 and current_time[5] == 0 or current_time[3] == 19 and current_time[4] == 23 and current_time[5] == 0:
            if not wlan.isconnected():
                sync_times_via_ntp()
                sleep(0.5)
            move_steps(steps_to_move)
            sleep(60*heating_time)
            move_steps(steps_to_move, clockwise=False)
            sleep(0.5)
            disconnect_wlan()
        sleep(1)

main()