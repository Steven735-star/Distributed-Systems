import zmq, pickle, sys, random

try:
    source_id = str(sys.argv[1])
    broker_ip = sys.argv[2]
    broker_in_port = sys.argv[3]
    num_jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 10
except Exception:
    print("Usage: python3 source.py <source_id> <broker_ip> <broker_in_port> [num_jobs]")
    sys.exit(1)

context = zmq.Context()
s = context.socket(zmq.PUSH)

try:
    s.connect(f"tcp://{broker_ip}:{broker_in_port}")

    for i in range(num_jobs):
        workload = random.randint(1, 100)
        s.send(pickle.dumps((source_id, workload)))

except Exception as e:
    print(f"[SOURCE ERROR] {e}")

finally:
    s.close()
    context.term()
