import JcSmartDevicePyd
import time
import cv2
import json
import numpy as np
import subprocess

def printRecvInfo(tNoti):
    strInfo = '[<--]CMD: %s, ret: %d, json: %s, error: %s.' % (
        tNoti.m_eReplyType.name, tNoti.m_nRet, tNoti.m_strJsonData, tNoti.m_strErrorInfo)
    print(strInfo)

vecDevList = JcSmartDevicePyd.SI_PyGetDeviceList()
nDevCnt = len(vecDevList)

if nDevCnt < 1:
    print('No device find.')
else:
    sDevSN = "FW151A001" # 设备 SN
    def waitForReply():
        """
        监听消息
        """
        while True:
            # 返回类型 int
            tNoti = JcSmartDevicePyd.JcNotify()

            ret = JcSmartDevicePyd.SI_PyGetNotify(sDevSN,tNoti)
            if ret == 0:
                # 接收回包
                printRecvInfo(tNoti)
                return tNoti
            else:
                time.sleep(0.001)

   #uninitialize
    # nRet = JcSmartDevicePyd.SI_PyUninit(sDevSN)
    # waitForReply()

    # set ring filter to clear
    color_filter_switch_script = "SwitchColorFilter.py"

    # X is red, Y is green, Z is blue, CF3 is clear
    subprocess.call(["python", color_filter_switch_script, "--filter", "X"])

    # initialize
    nRet = JcSmartDevicePyd.SI_PyInit(sDevSN)
    print('init', nRet)
    waitForReply()

    #set camera distance
    tParamMain = JcSmartDevicePyd.JcMainFlowParam()
    tParamMain.SetDistance(168)
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_CONFIG_PARAM,tParamMain)
    print("set distance", nRet)
    waitForReply()

    #get device info
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_GET_DEVICE_INFO)
    print('get device info', nRet)
    waitForReply()

    # set exposure time
    tParam = JcSmartDevicePyd.JcSetExpGainParam()
    tParam.m_nExp = 3500000
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN, JcSmartDevicePyd.eREQ_SET_EXPGAIN_VALUE, tParam)
    print("set Exposure Time", nRet)
    waitForReply()

    #take picture
    tParamSNAP = JcSmartDevicePyd.JcSetExpGainParam()
    start_time = time.time()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN, JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE, tParamSNAP)
    print("take picture", nRet)
    waitForReply()
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate the elapsed time in seconds
    print("Elapsed time:", elapsed_time, "seconds")

    #get image
    tParamMf1 = JcSmartDevicePyd.JcGetImg()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_GET_IMAGE_DATA,tParamMf1)
    print("get image", nRet)
    tNoti = waitForReply()

    tData = tNoti.m_pData

    mat = tData.m_tImage.copy()
    jsVal = json.loads(tNoti.m_strJsonData)
    print("mat dtype:{}".format(mat.dtype))

    dst = mat
    print("original max pixel: ", dst.max())

    # Normalize the pixel values between 0 and 1
    normalized_image = dst / dst.max()

    # Scale up the values to the 8-bit range (0-255)
    scaled_image = normalized_image * 255

    # Round the values to integers
    eight_bit_image = np.round(scaled_image).astype(np.uint8)

    print("new max pixel: ", eight_bit_image.max())
    #
    # jsVal = json.loads(tNoti.m_strJsonData)
    # nPixformat = JcSmartDevicePyd.Mono16
    # if "PixFormat" in jsVal:
    #     nPixformat = jsVal["PixFormat"]
    #
    # if mat.dtype == 'uint16':
    #     if nPixformat == JcSmartDevicePyd.Mono12:
    #         # dst = cv2.convertTo(mat, cv2.CV_16UC1, 16)
    #         mat *= 16
    #         dst = mat.astype(np.uint16)
    #     elif nPixformat == JcSmartDevicePyd.BayerRG12:
    #         # mat.convertTo(dst, cv2.CV_16UC1, 16)
    #         mat *= 16
    #         dst = mat.astype(np.uint16)
    #         # cv2.cvtColor(dst, dst, cv2.COLOR_BayerRG2RGB)
    #         dst = cv2.cvtColor(dst, cv2.COLOR_BayerRG2RGB)
    #     else:
    #         dst = mat.astype(np.uint16)

    cv2.imwrite("1.jpg", eight_bit_image)


