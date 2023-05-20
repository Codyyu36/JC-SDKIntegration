#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <winsock2.h>
#include <WS2tcpip.h> 

#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "127.0.0.1"  // Replace with the actual server IP address
#define SERVER_PORT 1234       // Replace with the actual server port

int main() {
    WSADATA wsaData;
    SOCKET sockfd;
    struct sockaddr_in serverAddr;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Failed to initialize Winsock." << std::endl;
        return 1;
    }

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
    serverAddr.sin_port = htons(SERVER_PORT);
    if (InetPton(AF_INET, SERVER_IP, &(serverAddr.sin_addr)) <= 0) {
        std::cerr << "Failed to set up server address." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Connect to the server
    if (connect(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cerr << "Failed to connect to the server." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Construct the IC command
    unsigned char data[] = { 0x02, 'I', 'C', 'C', 0, 0, 0x03 };
    int dataSize = sizeof(data);

    // Send the IC command to the server
    if (send(sockfd, (char*)data, dataSize, 0) == SOCKET_ERROR) {
        std::cerr << "Failed to send the IC command." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Receive the response from the server
    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));
    int bytesReceived = recv(sockfd, buffer, sizeof(buffer) - 1, 0);
    if (bytesReceived == SOCKET_ERROR) {
        std::cerr << "Failed to receive response from the server." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Process the response
    std::string response(buffer, bytesReceived);

    // Check if the response has all the fields
    if (response.length() < 7) {
        std::cerr << "Invalid response from the server. Missing fields." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Extract the fields from the response
    unsigned char stx = response[0];
    std::string command = response.substr(1, 2);
    std::string cmdType = response.substr(3, 1);
    std::string acknowledge = response.substr(4, 1);
    std::string reserve = response.substr(5, 1);
    unsigned char etx = response[6];

    // Check if the response has the correct format
    if (stx != 0x02 || command != "IC" || etx != 0x03) {
        std::cerr << "Invalid response from the server. Incorrect format." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Check if the connection was successful (Acknowledge = 0)
    if (acknowledge != "0") {
        std::cerr << "NG response from the server. Invalid Acknowledge value. Connection is not established." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Close the socket and clean up Winsock
    closesocket(sockfd);
    WSACleanup();

    return 0;
}
