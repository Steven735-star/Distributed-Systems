from socket import *
import threading
import time

# Function to handle each client connection individually
def handle_client(connectionSocket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            # Receive data (buffer size 1024)
            message = connectionSocket.recv(1024).decode()
            
            # If message is empty, the client closed the connection
            if not message:
                break
            
            print(f"[{addr}] Sent: {message}")
            
            # Process the message (Capitalize it)
            modifiedMessage = message.upper()
            
            # Simulate some processing time to demonstrate concurrency
            time.sleep(1) 
            
            # Send response back
            connectionSocket.send(modifiedMessage.encode())
            
    except ConnectionResetError:
        print(f"[{addr}] Connection lost unexpectedly.")
    finally:
        connectionSocket.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    # Allow port reuse to avoid "Address already in use" errors
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    # Bind to all available interfaces
    serverSocket.bind(("", serverPort))
    
    serverSocket.listen(5)
    print(f"[LISTENING] Server is listening on port {serverPort}")

    while True:
        # Accept new connection
        connectionSocket, addr = serverSocket.accept()
        
        # Create a new thread for the client
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        thread.start()
        
        # Display active connections (subtracting 1 for the main thread)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()