import JcSmartDevicePyd
import time
import cv2

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

    #check version
    version_num = 'version: ' + JcSmartDevicePyd.SI_PyGetVersion()
    print("version", version_num)
    #
    #uninitialize
    # nRet = JcSmartDevicePyd.SI_PyUninit(sDevSN)

    # initialize
    nRet = JcSmartDevicePyd.SI_PyInit(sDevSN)
    print('init', nRet)
    waitForReply()

    #get device info
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_GET_DEVICE_INFO)
    print('get device info', nRet)
    waitForReply()

    #set exposure time
    tParam = JcSmartDevicePyd.JcSetExpGainParam()
    tParam.m_nExp = 5500
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_EXPGAIN_VALUE,tParam)
    print("set Exposure Time", nRet)
    waitForReply()

    # TODO: set ring filter to "clear"
    # tParamMain = JcSmartDevicePyd.JcMainFlowParam()
    #

    #take picture
    tParamSNAP = JcSmartDevicePyd.JcSetExpGainParam()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE,tParamSNAP)
    print("take picture", nRet)
    waitForReply()

    #get image
    tParamMf1 = JcSmartDevicePyd.JcGetImg()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_GET_IMAGE_DATA,tParamMf1)
    print("get image", nRet)
    tNoti = waitForReply()

    tData = tNoti.m_pData

    mat = tData.m_tImage.copy()

    cv2.imwrite("1.jpg", mat)


