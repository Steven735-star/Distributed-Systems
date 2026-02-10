#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12000
#define SERVER_IP "127.0.0.1"   // Change to server IP if running remotely

int main() {
    int sock;
    struct sockaddr_in server;
    char message[1000], server_reply[2000];
    int n;

    // Create TCP socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("Could not create socket");
        return 1;
    }
    puts("Socket created");

    // Server address configuration
    server.sin_addr.s_addr = inet_addr(SERVER_IP);
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);

    // Connect to the server
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("Connection failed");
        close(sock);
        return 1;
    }
    puts("Connected to server\n");

    // Communication loop
    while (1) {
        printf("Enter message (or 'exit' to quit): ");

        // Read a full line (including spaces and newline)
        if (fgets(message, sizeof(message), stdin) == NULL)
            break;

        // Exit condition
        if (strcmp(message, "exit\n") == 0)
            break;

        // Send full message (newline is used as delimiter)
        if (send(sock, message, strlen(message), 0) < 0) {
            perror("Send failed");
            break;
        }

        // Receive server response
        n = recv(sock, server_reply, sizeof(server_reply) - 1, 0);
        if (n <= 0) {
            puts("Server disconnected");
            break;
        }

        server_reply[n] = '\0';
        printf("Server reply: %s\n", server_reply);
    }

    close(sock);
    return 0;
}
