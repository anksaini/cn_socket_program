#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main(){
  //Message to clients
  char serv_message[256] = "You have reached the server";

  //create server socket
  int serv_soc;
  serv_soc = socket(AF_INET, SOCK_STREAM, 0);

  //define the server address
  struct sockaddr_in serv_address;
  serv_address.sin_family = AF_INET;
  serv_address.sin_port = htons(9001);
  serv_address.sin_addr.s_addr = INADDR_ANY;

  //bind the socket to specified IP & port
  bind(serv_soc, (struct sockaddr*) &serv_address, sizeof(serv_address));

  //Begin listenning
  listen(serv_soc,5);

  //Accept Client socket
  int client_soc;
  client_soc = accept(serv_soc, NULL, NULL);

  //Send message to client
  send(client_soc, serv_message, sizeof(serv_message), 0);

  //close the socket
  close(serv_soc);

  return 0;
}
