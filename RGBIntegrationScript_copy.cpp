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

    unsigned char IC_response_stx = IC_response[0];
    std::string IC_response_command = IC_response.substr(1, 2);
    std::string IC_response_cmdType = IC_response.substr(3, 1);
    std::string IC_response_acknowledge = IC_response.substr(4, 1);
    std::string IC_response_reserve = IC_response.substr(5, 1);
    unsigned char IC_response_etx = IC_response[6];

    // Check if the IC response has the correct format
    if (IC_response_stx != 0x02 || IC_response_command != "IC" || IC_response_etx != 0x03) {
        std::cerr << "Invalid response from the server. Incorrect format." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Check if the IC was successful (Acknowledge = 0)
    if (IC_response_acknowledge != "0") {
        std::cerr << "NG response from the server. Invalid Acknowledge value. Connection is not established." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Construct the NEXT command
    char NEXT_command[] = "NEXT";
    int next_or_prev = 0; //0 is next, 1 is previous

    // Concatenate the data elements into a single string
    std::string NEXT_data;
    NEXT_data += STX;
    NEXT_data += NEXT_command;
    NEXT_data += cmdType;
    NEXT_data += acknowledge;
    NEXT_data += reserve;
    NEXT_data += rackNo;
    NEXT_data += pgNo;
    NEXT_data += chanNo;
    NEXT_data += next_or_prev; 
    NEXT_data += ETX;

    // Send the NEXT command to the server
    if (send(sockfd, NEXT_data.c_str(), IC_dataSize, 0) == SOCKET_ERROR) {
        std::cerr << "Failed to send the IC command." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Receive the NEXT response from the server
    char NEXT_buffer[1024];
    memset(NEXT_buffer, 0, sizeof(NEXT_buffer));
    bytesReceived = recv(sockfd, NEXT_buffer, sizeof(NEXT_buffer) - 1, 0);
    if (bytesReceived == SOCKET_ERROR) {
        std::cerr << "Failed to receive response from the server." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Process the NEXT response
    std::string NEXT_response(NEXT_buffer, bytesReceived);

    // Check if the response has all the fields
    if (NEXT_response.length() < 10) {
        std::cerr << "Invalid response from the server. Missing fields." << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return 1;
    }

    // Extract the fields from the IC response
    std::cout << "NEXT Response: " << NEXT_response << std::endl;

    // Close the socket and clean up Winsock
    closesocket(sockfd);
    WSACleanup();

    return 0;
}