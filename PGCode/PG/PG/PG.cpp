#include <winsock2.h>
#include <WS2tcpip.h>
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cstdio>

#define SERVER_IP "192.168.10.1"  // Replace with the actual server IP address
// 192.168.10.1
#define SERVER_PORT 21 // reference the manual 服务端监听端口固定为9999

int main() {
    WSADATA wsaData;
    SOCKET sockfd;
    struct sockaddr_in serverAddr;
    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Failed to initialize Winsock." << std::endl;
        return 1;
    }
    std::cout << "Hello, world!" << std::endl;

    // Create socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == INVALID_SOCKET) {
        std::cerr << "Failed to create socket." << std::endl;
        WSACleanup();
        return 1;
    }

    // Set up server address
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;

    //set server ip
    if (inet_pton(AF_INET, SERVER_IP, &(serverAddr.sin_addr)) != 1) {
        std::cerr << "Invalid server IP address." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    serverAddr.sin_port = htons(SERVER_PORT);

    // Connect to the server
    if (connect(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        WSAGetLastError();
        std::cerr << "Failed to connect to the server." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Construct the IC command
    unsigned char STX = 0x02;
    unsigned char ETX = 0x03;
    char IC_command[] = "IC";
    char cmdType[] = "C";
    char acknowledge[] = "";
    char reserve[] = "";
    int rackNo = 1;
    int pgNo = 1;
    int chanNo = 1;

    // Concatenate the data elements into a single string
    std::string IC_data;
    IC_data += STX;
    IC_data += IC_command;
    IC_data += cmdType;
    IC_data += acknowledge;
    IC_data += reserve;
    IC_data += ETX;

    int IC_dataSize = sizeof(IC_data);

    // Send the IC command to the server
    if (send(sockfd, IC_data.c_str(), IC_dataSize, 0) == SOCKET_ERROR) {
        std::cerr << "Failed to send the IC command." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Receive the IC response from the server
    char IC_buffer[1024];
    memset(IC_buffer, 0, sizeof(IC_buffer));
    int bytesReceived = recv(sockfd, IC_buffer, sizeof(IC_buffer) - 1, 0);
    if (bytesReceived == SOCKET_ERROR) {
        std::cerr << "Failed to receive response from the server." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Process the IC response
    std::string IC_response(IC_buffer, bytesReceived);

    // Check if the response has all the fields
    if (IC_response.length() < 10) {
        std::cerr << "Invalid response from the server. Missing fields." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Extract the fields from the IC response
    std::cout << "ICResponse: " << IC_response << std::endl;


    // Close the socket and clean up Winsock
    closesocket(sockfd);
    WSACleanup();

    return 0;
}