import zmq, pickle, sys

bind_ip = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
in_port = sys.argv[2] if len(sys.argv) > 2 else "5555"
out_port = sys.argv[3] if len(sys.argv) > 3 else "5556"

context = zmq.Context()

try:
    inp = context.socket(zmq.PULL)
    out = context.socket(zmq.PUSH)

    inp.bind(f"tcp://{bind_ip}:{in_port}")
    out.bind(f"tcp://{bind_ip}:{out_port}")

    print(f"[BROKER] IN  tcp://{bind_ip}:{in_port}")
    print(f"[BROKER] OUT tcp://{bind_ip}:{out_port}")

    while True:
        try:
            msg = inp.recv()
            out.send(msg)
        except Exception as e:
            print(f"[BROKER ERROR] {e}")

except KeyboardInterrupt:
    print("\n[BROKER] Shutting down...")
finally:
    inp.close()
    out.close()
    context.term()
