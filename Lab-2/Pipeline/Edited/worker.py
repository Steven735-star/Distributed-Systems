import zmq, pickle, sys, time

try:
    worker_id = str(sys.argv[1])
    broker_ip = sys.argv[2]
    broker_out_port = sys.argv[3]
except Exception:
    print("Usage: python3 worker.py <worker_id> <broker_ip> <broker_out_port>")
    sys.exit(1)

context = zmq.Context()
r = context.socket(zmq.PULL)

try:
    r.connect(f"tcp://{broker_ip}:{broker_out_port}")

    count = 1
    while True:
        try:
            source_id, work = pickle.loads(r.recv())
            print(f"[Worker {worker_id}] job#{count} from Source {source_id} workload={work}", flush=True)
            count += 1
            time.sleep(work * 0.01)
        except Exception as e:
            print(f"[WORKER {worker_id} ERROR] {e}")

except KeyboardInterrupt:
    print(f"\n[Worker {worker_id}] Shutting down...")

finally:
    r.close()
    context.term()
