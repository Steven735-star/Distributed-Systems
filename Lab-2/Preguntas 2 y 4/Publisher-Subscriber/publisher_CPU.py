import zmq
import time
import psutil
import platform
from datetime import datetime

context = zmq.Context()
s = context.socket(zmq.PUB)

HOST = '0.0.0.0'
PORT = '5000'
hostname = platform.node()

p = f"tcp://{HOST}:{PORT}"
try:
    s.bind(p)
    print(f"CPU Service started on {hostname} at port {PORT}")

    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        # Obtenemos la hora con milisegundos para mayor precisión
        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Tópico: CPU
        message = f"CPU [{hostname}] at {now}: {cpu_percent}%"
        s.send_string(message)
        time.sleep(0.5) # Un poco más rápido para ver el flujo
except Exception as e:
    print(f"Error: {e}")