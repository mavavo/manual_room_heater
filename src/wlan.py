import network
import time
from hidden import My_SSID, My_PASSWORD
import ntptime

SSID = My_SSID
PASSWORD = My_PASSWORD

wlan = network.WLAN(network.WLAN.IF_STA)

def connect_wlan(timeout=15):
    'Connects to configured wlan network and returns the wlan interface.'
    network.country('DE')
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        start = time.ticks_ms()

        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), start) > timeout * 1000:
                raise RuntimeError("wlan timeout")
            time.sleep_ms(200)
    return wlan

def sync_times_via_ntp():
    'Synchronizes the RTC and UTC via NTP and returns wlan interface.'
    wlan = connect_wlan()
    ntptime.settime()   # Gets UTC from internet and sets RTC (real time clock) of Pico to this UTC (coordinated universal time) 
    return wlan

def disconnect_wlan():
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep_ms(500)