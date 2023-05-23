// CameraCodeFW151.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "SI_Interface.h"
#include "SI_CmParam.h"
#include "SI_ErrorCode.h"
#include "SI_ParmsBase.h"
#include <iostream>
#include <memory>


int main()
{
    
    // Try getting the version of the SDK
    std::cout << JC::SI_GetVersion();

    // Try initializing 
    JC::SI_Handle handle = std::make_shared<JC::JcSmartDevInterface>();
    JC::JcRequestCMDPtr param = std::make_shared<JC::JcRequestCMD>();
    param->m_pData = std::make_shared<JC::JcInitDevice>("");
    JC::JcInitDevicePtr pParam = std::dynamic_pointer_cast<JC::JcInitDevice>(param->m_pData);
    int nRet = SI_Init(handle, param);

    std::cout << nRet;
    // Try the SI_GetDeviceList() function
    std::vector<JC::DeviceInfo> deviceList = JC::SI_GetDeviceList();

}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
