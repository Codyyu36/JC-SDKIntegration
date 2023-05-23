#include <winsock2.h>
#include <WS2tcpip.h>
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cstdio>

#define SERVER_IP "192.168.10.1"  // Replace with the actual server IP address
// 192.168.10.1
#define SERVER_PORT 9999 // reference the manual 服务端监听端口固定为9999

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
    unsigned char IC_data[] = { 0x02, 'I', 'C', 'C', 0, 0, 0x03 };
    int IC_dataSize = sizeof(IC_data);

    // Send the IC command to the server
    if (send(sockfd, (char*)IC_data, IC_dataSize, 0) == SOCKET_ERROR) {
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
    if (IC_response.length() < 7) {
        std::cerr << "Invalid response from the server. Missing fields." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Extract the fields from the IC response
    std::cout << "Response: " << IC_response << std::endl;

    unsigned char stx = IC_response[0];
    std::string command = IC_response.substr(1, 2);
    std::string cmdType = IC_response.substr(3, 1);
    std::string acknowledge = IC_response.substr(4, 1);
    std::string reserve = IC_response.substr(5, 1);
    unsigned char etx = IC_response[6];

    // Check if the IC response has the correct format
    if (stx != 0x02 || command != "IC" || etx != 0x03) {
        std::cerr << "Invalid response from the server. Incorrect format." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Check if the IC was successful (Acknowledge = 0)
    if (acknowledge != "0") {
        std::cerr << "NG response from the server. Invalid Acknowledge value. Connection is not established." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Construct the NEXT command
    char NEXT_data[] = { 0x02, 'N', 'E', 'X', 'T', 'C', 0, 0, 1, 1, 1, 0, 0x03 };
    int NEXT_dataSize = sizeof(NEXT_data);

    // Send the IC command to the server
    if (send(sockfd, (char*)IC_data, IC_dataSize, 0) == SOCKET_ERROR) {
        std::cerr << "Failed to send the IC command." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Receive the IC response from the server
    char buffer[1024];
    memset(IC_buffer, 0, sizeof(IC_buffer));
    int bytesReceived = recv(sockfd, IC_buffer, sizeof(IC_buffer) - 1, 0);
    if (bytesReceived == SOCKET_ERROR) {
        std::cerr << "Failed to receive response from the server." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }


    // Close the socket and clean up Winsock
    closesocket(sockfd);
    WSACleanup();

    return 0;
}