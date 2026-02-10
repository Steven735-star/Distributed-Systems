from socket import *
import random
import string
import time

def get_random_string(length=8):
    # Generate a random lowercase string of fixed length
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# --- CONFIGURATION ---
# Use "localhost" for local testing.
# Use the SERVER IP address (e.g., "172.23.208.74") for remote testing.
serverName = "localhost"
serverPort = 12000

try:
    # Create a TCP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    # Connect to the server
    clientSocket.connect((serverName, serverPort))
    print(f"Connected to server at {serverName}:{serverPort}")

    # Generate a random number of messages between 5 and 10
    num_messages = random.randint(5, 10)
    print(f"--- Starting transmission of {num_messages} messages ---")

    for i in range(num_messages):
        message = get_random_string()
        print(f"Sending ({i+1}/{num_messages}): {message}")
        
        # Send message to the server
        clientSocket.send(message.encode())
        
        # Wait for server response
        modifiedSentence = clientSocket.recv(1024)
        print(f"Received from server: {modifiedSentence.decode()}")
        
        # Small delay for better visualization of concurrency
        time.sleep(0.5)

    print("--- Transmission finished ---")
    
    # Close the socket connection
    clientSocket.close()

except ConnectionRefusedError:
    print("Error: Could not connect to the server. Is it running?")
