import JcSmartDevicePyd
import time

class CameraClient:
    def __init__(self, devSN):
        self.devSN = devSN

    def waitForReply(self):
        """
        监听消息
        """
        while True:
            tNoti = JcSmartDevicePyd.JcNotify()

            ret = JcSmartDevicePyd.SI_PyGetNotify(self.devSN, tNoti)
            if ret == 0:
                # 接收回包
                print("tNoti received: {}".format(tNoti))
                break
            else:
                time.sleep(0.001)

    def initializeDevice(self):
        version_num = 'version: ' + JcSmartDevicePyd.SI_PyGetVersion()
        print("version", version_num)
        self.waitForReply()

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
        nRet = JcSmartDevicePyd.SI_PyOperations(self.devSN, JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE, tParamSNAP)
        print("take picture", nRet)
        self.waitForReply()

    def getImageData(self):
        tParamMf1 = JcSmartDevicePyd.JcGetImg()
        nRet = JcSmartDevicePyd.SI_PyOperations(self.devSN, JcSmartDevicePyd.eREQ_GET_IMAGE_DATA, tParamMf1)
        print("get image", nRet)
        self.waitForReply()

