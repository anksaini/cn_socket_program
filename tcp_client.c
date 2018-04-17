#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main(){
  //create a socket
  int soc;
  soc = socket(AF_INET, SOCK_STREAM, 0);

  //specify an address for the socket
  struct sockaddr_in serv_address;
  serv_address.sin_family = AF_INET;
  serv_address.sin_port = htons(9001);
  serv_address.sin_addr.s_addr = INADDR_ANY;

  //Connection Status
  int con_status = connect(soc, (struct sockaddr*)&serv_address,sizeof(serv_address));
  if (con_status == -1){
    printf("Connection Failed\n");
  }

  //Recieve Data from the server
  char serv_resp[256];
  recv(soc, &serv_resp, sizeof(serv_resp), 0);

  //print the server's response
  printf("Server's Response: %s\n",serv_resp);

  //close the socket
  close(soc);

  return 0;
}
