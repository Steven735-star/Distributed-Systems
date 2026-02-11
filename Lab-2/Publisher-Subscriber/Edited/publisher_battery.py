import zmq
import time
import psutil
import platform
from datetime import datetime

context = zmq.Context()
s = context.socket(zmq.PUB)

HOST = '0.0.0.0'
PORT = '5001'
hostname = platform.node()

p = f"tcp://{HOST}:{PORT}"
try:
    s.bind(p)
    print(f"Battery Service started on {hostname} at port {PORT}")

    while True:
        battery = psutil.sensors_battery()
        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        if battery is not None:
            percent = battery.percent
            plugged = "Plugged In" if battery.power_plugged else "On Battery"
            message = f"BATTERY [{hostname}] at {now}: {percent}% ({plugged})"
            s.send_string(message)
        
        time.sleep(5)
except Exception as e:
    print(f"Error: {e}")