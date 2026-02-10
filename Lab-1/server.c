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

// Global variables for client tracking
int client_count = 0;
pthread_mutex_t count_mutex = PTHREAD_MUTEX_INITIALIZER;

void *handle_client(void *socket_desc) {
    int sock = *(int*)socket_desc;
    free(socket_desc);
    char buffer[BUFFER_SIZE];
    int read_size;

    // Communication loop for a single client
    while ((read_size = recv(sock, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[read_size] = '\0';
        
        // Print message received
        printf("Client says: %s", buffer);

        // Convert to uppercase
        for (int i = 0; buffer[i]; i++) {
            buffer[i] = toupper((unsigned char)buffer[i]);
        }

        // Send response back
        send(sock, buffer, strlen(buffer), 0);
        
        // Clear buffer
        memset(buffer, 0, BUFFER_SIZE);
    }

    // Client disconnected
    close(sock);
    
    // Decrease client count safely
    pthread_mutex_lock(&count_mutex);
    client_count--;
    printf("\nA client disconnected. Active clients: %d\n", client_count);
    pthread_mutex_unlock(&count_mutex);

    pthread_exit(NULL);
}

int main() {
    int socket_desc, client_sock, c;
    struct sockaddr_in server, client;

    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_desc == -1) {
        perror("Could not create socket");
        return 1;
    }

    int opt = 1;
    setsockopt(socket_desc, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(PORT);

    if (bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("Bind failed");
        close(socket_desc);
        return 1;
    }

    listen(socket_desc, 5);
    printf("Server listening on port %d...\n", PORT);
    printf("Waiting for incoming connections...\n");

    c = sizeof(struct sockaddr_in);

    while ((client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c))) {
        
        // Increase client count safely
        pthread_mutex_lock(&count_mutex);
        client_count++;
        printf("\nConnection accepted. Active clients: %d\n", client_count);
        pthread_mutex_unlock(&count_mutex);

        pthread_t thread_id;
        int *new_sock = malloc(sizeof(int));
        *new_sock = client_sock;

        if (pthread_create(&thread_id, NULL, handle_client, (void*) new_sock) < 0) {
            perror("Could not create thread");
            free(new_sock);
        }

        pthread_detach(thread_id); 
    }

    if (client_sock < 0) {
        perror("Accept failed");
        close(socket_desc);
        return 1;
    }

    return 0;
}