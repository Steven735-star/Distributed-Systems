#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <pthread.h>

#define PORT 12000
#define BUFFER_SIZE 1024

/*
 * Thread function that handles communication with a single client.
 * It receives data until a newline character ('\n') is detected,
 * then processes the complete message and sends back a response.
 */
void *handle_client(void *socket_desc) {
    int sock = *(int*)socket_desc;
    free(socket_desc);

    char buffer[BUFFER_SIZE];
    char message[BUFFER_SIZE * 2] = {0};
    int read_size;

    // Receive data until newline is found
    while ((read_size = recv(sock, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[read_size] = '\0';
        strcat(message, buffer);

        // Newline indicates end of message
        if (strchr(buffer, '\n') != NULL) {
            break;
        }
    }

    if (read_size <= 0) {
        close(sock);
        pthread_exit(NULL);
    }

    printf("Client says: %s", message);

    // Convert the entire message to uppercase
    for (int i = 0; message[i]; i++) {
        message[i] = toupper((unsigned char)message[i]);
    }

    // Send the response back to the client
    send(sock, message, strlen(message), 0);

    close(sock);
    printf("Client disconnected\n");
    pthread_exit(NULL);
}

int main() {
    int socket_desc, client_sock, c;
    struct sockaddr_in server, client;

    // Create TCP socket
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_desc == -1) {
        perror("Could not create socket");
        return 1;
    }

    // Allow socket reuse to avoid TIME_WAIT issues
    int opt = 1;
    setsockopt(socket_desc, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // Server address configuration
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(PORT);

    // Bind socket to port
    if (bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("Bind failed");
        close(socket_desc);
        return 1;
    }

    // Start listening for incoming connections
    listen(socket_desc, 5);
    puts("Waiting for incoming connections...");

    c = sizeof(struct sockaddr_in);

    // Accept clients indefinitely
    while ((client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c))) {
        puts("Connection accepted");

        pthread_t thread_id;
        int *new_sock = malloc(sizeof(int));
        *new_sock = client_sock;

        // Create a new thread for each client
        if (pthread_create(&thread_id, NULL, handle_client, (void*) new_sock) < 0) {
            perror("Could not create thread");
            free(new_sock);
        }

        // Detach thread to avoid zombie threads
        pthread_detach(thread_id);
    }

    if (client_sock < 0) {
        perror("Accept failed");
        close(socket_desc);
        return 1;
    }

    close(socket_desc);
    return 0;
}
