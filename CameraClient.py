import JcSmartDevicePyd
import time
import cv2
import json
import numpy as np

class CameraClient:
    def __init__(self, devSN):
        self.devSN = devSN

    @staticmethod
    def printRecvInfo(tNoti):
        strInfo = '[<--]CMD: %s, ret: %d, json: %s, error: %s.' % (
            tNoti.m_eReplyType.name, tNoti.m_nRet, tNoti.m_strJsonData, tNoti.m_strErrorInfo)
        print(strInfo)

    def waitForReply(self):
        """
        监听消息
        """
        while True:
            # 返回类型 int
            tNoti = JcSmartDevicePyd.JcNotify()

            ret = JcSmartDevicePyd.SI_PyGetNotify(self.devSN, tNoti)
            if ret == 0:
                # 接收回包
                self.printRecvInfo(tNoti)
                return tNoti
            else:
                time.sleep(0.001)

    def initializeDevice(self):
        version_num = 'version: ' + JcSmartDevicePyd.SI_PyGetVersion()
        print("version", version_num)

        nRet = JcSmartDevicePyd.SI_PyInit(self.devSN)
        print('init', nRet)
        self.waitForReply()

    def getDeviceInfo(self):
        nRet = JcSmartDevicePyd.SI_PyOperations(self.devSN, JcSmartDevicePyd.eREQ_GET_DEVICE_INFO)
        print('get device info', nRet)
        self.waitForReply()

    def setExposureTime(self, exposure):
        tParam = JcSmartDevicePyd.JcSetExpGainParam()
        tParam.m_nExp = exposure
        nRet = JcSmartDevicePyd.SI_PyOperations(self.devSN, JcSmartDevicePyd.eREQ_SET_EXPGAIN_VALUE, tParam)
        print("set Exposure Time", nRet)
        self.waitForReply()

    def takePicture(self):
        tParamSNAP = JcSmartDevicePyd.JcSetExpGainParam()
        start_time = time.time()
        nRet = JcSmartDevicePyd.SI_PyOperations(self.devSN, JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE, tParamSNAP)
        print("take picture", nRet)
        self.waitForReply()
        end_time = time.time()
        elapsed_time = end_time - start_time  # Calculate the elapsed time in seconds
        print("Elapsed time:", elapsed_time, "seconds")

    def getImageData(self, index):
        tParamMf1 = JcSmartDevicePyd.JcGetImg()
        nRet = JcSmartDevicePyd.SI_PyOperations(self.devSN, JcSmartDevicePyd.eREQ_GET_IMAGE_DATA, tParamMf1)
        print("get image", nRet)
        tNoti = self.waitForReply()

        tData = tNoti.m_pData
        # 图像数据
        mat = tData.m_tImage.copy()
        dst = mat
        
        cv2.imwrite("{}.jpg".format(index), dst)

    # TODO: add swapping filter wheel after API is available