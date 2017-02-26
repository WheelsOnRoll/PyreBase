#include<stdio.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>

#define PORT 8134
//#define ADDR "127.0.0.1"
//#define ADDR "10.100.12.27"
#define ADDR "0.0.0.0"

int main(){
	int serverId, clientId;
	char buffer[1024];
	struct sockaddr_in serverAddress;
	struct sockaddr_storage serverStorage;
	socklen_t address_size;

	// Create socket
	serverId = socket(PF_INET, SOCK_STREAM, 0);

	// Set server address
	serverAddress.sin_family = AF_INET;
	serverAddress.sin_port = PORT;
	serverAddress.sin_addr.s_addr = inet_addr(ADDR);
	memset(serverAddress.sin_zero, '\0', sizeof serverAddress.sin_zero); 

	// Bind server to address
	bind(serverId, (struct sockaddr *) &serverAddress, sizeof(serverAddress));

	// Start listening
	if(listen(serverId, 5) == 0)
		printf("Listening at %s:%d\n", ADDR, PORT);
	else
		printf("Error starting the server...\n");
	fflush(stdout);
	
	// Accept client request
	address_size = sizeof serverStorage;
	clientId = accept(serverId, (struct sockaddr *) &serverStorage, &address_size);

	if(clientId<0)
		printf("Error\n");
	else
		printf("Client connected successfully\n");
	fflush(stdout);
	
	while(1){
		char c;
		scanf("%c", &c);
		fflush(stdin);
		//Send message to client
		if(c=='1')
			strcpy(buffer, "1\n");
		else
			strcpy(buffer, "0\n");
		send(clientId, buffer, 2, 0);

		memset(buffer,0,strlen(buffer));
		recv(clientId, buffer, 1024, 0);
		printf("Client: %s\n", buffer);
		fflush(stdout);
	}

	// Close the server
	close(serverId);

	return 0;
}
