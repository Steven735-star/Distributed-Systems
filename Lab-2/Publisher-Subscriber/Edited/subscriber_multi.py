import zmq
from datetime import datetime

context = zmq.Context()
s = context.socket(zmq.SUB)

s.connect("tcp://localhost:5000")
s.connect("tcp://172.23.198.151:5001")

s.setsockopt_string(zmq.SUBSCRIBE, "CPU")
s.setsockopt_string(zmq.SUBSCRIBE, "BATTERY")

print("Subscriber connected. Comparing timestamps...")

while True:
    try:
        message = s.recv_string()
        # Hora local del suscriptor al recibir
        t_recv = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{t_recv}] Received -> {message}")
    except KeyboardInterrupt:
        break