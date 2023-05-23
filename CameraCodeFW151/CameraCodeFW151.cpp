// CameraCodeFW151.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "SI_Interface.h"
#include "SI_CmParam.h"
#include "SI_ErrorCode.h"
#include "SI_ParmsBase.h"
#include <iostream>
#include <memory>
#include <future>

JC::SI_Handle m_pHandle;
std::atomic<bool> bStop(false);

void RecvMessage()
{
    while (true)
    {
        if (bStop) // Break out of the message loop
        {
            break;
        }

        JC::JcNotifyPtr retparam = std::make_shared<JC::JcNotify>();
        int nRet = SI_GetNotify(m_pHandle, retparam);
        JC::JcNotify param = *retparam;

        if (nRet == SI_ALL_SUCCESS)
        {
            // TODO: Parse and handle the returned message
            // Specific actions based on the received message can be implemented here
        }
        else if (nRet == SI_ALL_ERROR)
        {
            // Handle the error case
            std::cout << "Error: Operation failed." << std::endl;
        }
        else if (nRet == SI_ALL_BYPASS)
        {
            // Handle the bypass case
            std::cout << "Warning: Bypassing current operation." << std::endl;
        }
        else if (nRet == SI_ALL_TIMEOUT)
        {
            // Handle the timeout case
            std::cout << "Error: Operation timed out." << std::endl;
        }
        else if (nRet == SI_ALL_BUSYNOW)
        {
            // Handle the busy case
            std::cout << "Warning: Previous operation not completed." << std::endl;
        }
        else if (nRet == SI_ALL_ERRORDATA)
        {
            // Handle the error data type case
            std::cout << "Error: Operation not compatible with data type." << std::endl;
        }
        else
        {
            // Handle any other error codes or unknown values of nRet
            std::cout << "Unknown error occurred." << std::endl;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }
}

int main()
{
    
    // Try getting the version of the SDK
    std::cout << JC::SI_GetVersion();

    // Try initializing 
    JC::JcRequestCMDPtr param = std::make_shared<JC::JcRequestCMD>();
    param->m_pData = std::make_shared<JC::JcInitDevice>("");
    JC::JcInitDevicePtr pParam = std::dynamic_pointer_cast<JC::JcInitDevice>(param->m_pData);
    int nRet = SI_Init(m_pHandle, param);
    if (nRet != 0) {
        std::cout << JC::SI_GetVersion();
        return 1;
    }

    // Try the SI_GetDeviceList() function
    std::vector<JC::DeviceInfo> deviceList = JC::SI_GetDeviceList();

    // Asynchronously call the RecvMessage function
    std::future<void> asyncTask = std::async(std::launch::async, &RecvMessage);

    // Do other work in parallel with RecvMessage

    // Wait for the async task to finish
    asyncTask.get();

    ///< 1.构建任务命令的智能指针
    JC::JcRequestCMDPtr cmParam =
        std::make_shared<JC::JcRequestCMD>(JC::JcRequestCMD::eREQ_SET_CONFIG_PARAM);
    ///< 2.为设置输入参数分配内存
    cmParam->m_pData = std::make_shared<JC::JcMainFlowParam>();
    ///< 3.创建一个智能指针指向传入参数的内存地址
    // 1、设置模式为测量模式
    int MeasPatternNum = 4; // 待测量画面数量
    JC::JcFlowPtnsParam flowParam = JC::JcFlowPtnsParam(JC::JcFlowPtnsParam::eChromMeasure,
        MeasPatternNum, eSignal); //what is this?
    // 2、设置当前工作距离
    JC::JcMainFlowParamPtr camParam = std::dynamic_pointer_cast<JC::JcMainFlowParam>
        (cmParam->m_pData);
    camParam->SetDistance(900);
    // 4、为每个画面设置光学参数
    for (int i = 0; i < MeasPatternNum; i++)
    {
        // 4.1、设置单个待测量画面的光圈
        std::vector<JC::JcPatternParam>& vecPtnParam = flowParam.GetPtnList();
        vecPtnParam.at(i).m_nAperture = 8.0;
        // 4.2、设置单个待测量画面的标定文件
        vecPtnParam.at(i).m_strCalibFile = "Common.csv";
        for (int j = 0; j < vecPtnParam.at(i).GetTaskList().size(); j++)
        {
            // 4.3、设置画面对应滤镜的初始参数（曝光、增益、FT 及自动曝光参数）
            std::vector<JC::JcTaskParam>& tPtnParam = vecPtnParam.at(i).GetTaskList();
            tPtnParam.at(j).m_nExp = 50000;
        }
    }
    camParam->SetFlowParam(flowParam);
    // 5 下发参数
    int nRet = SI_Operations(m_pHandle, cmParam);


    std::cout << nRet;

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
