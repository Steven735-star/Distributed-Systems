#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>

#define PORT 12000
#define SERVER_IP "192.168.68.126" 

// Function to generate a random string of a given length
void get_random_string(char *str, int length) {
    char charset[] = "abcdefghijklmnopqrstuvwxyz";
    for (int n = 0; n < length; n++) {
        int key = rand() % (int)(sizeof(charset) - 1);
        str[n] = charset[key];
    }
    str[length] = '\0';
}

int main(int argc, char *argv[]) {
    int sock;
    struct sockaddr_in server;
    char message[9], server_reply[1024];

    // Initialize random seed
    srand(time(NULL));

    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        printf("Could not create socket\n");
        return 1;
    }

    server.sin_addr.s_addr = inet_addr(SERVER_IP);
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);

    // Connect to remote server
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("Connection failed. Error");
        return 1;
    }
    printf("Connected to server at %s:%d\n", SERVER_IP, PORT);

    // Generate a random number of messages between 5 and 10
    int num_messages = (rand() % 6) + 5;
    printf("--- Starting automated transmission of %d messages ---\n", num_messages);

    for (int i = 0; i < num_messages; i++) {
        get_random_string(message, 8);
        printf("Sending (%d/%d): %s\n", i + 1, num_messages, message);

        // Send data
        if (send(sock, message, strlen(message), 0) < 0) {
            puts("Send failed");
            return 1;
        }

        // Receive reply
        int read_size = recv(sock, server_reply, 1024, 0);
        if (read_size < 0) {
            puts("Recv failed");
            break;
        }
        
        server_reply[read_size] = '\0'; 
        printf("Received from server: %s\n", server_reply);

        // Small delay to simulate real-time traffic (0.5 seconds)
        usleep(500000);
    }

    printf("--- Transmission finished ---\n");
    close(sock);
    return 0;
}