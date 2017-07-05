#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <MQTTClient.h>

#define CLIENTID	"Example"
#define ADDRESS		"tcp://localhost:1883"

int main()
{
	MQTTClient client;
	MQTTClient_create(&client, ADDRESS, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL);
	printf("Client created\n");
	MQTTClient_destroy(&client);
	printf("Client destroyed\n");

	return 0;
}
