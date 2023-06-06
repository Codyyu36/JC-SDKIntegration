import JcSmartDevicePyd
import time

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
                print("tNoti: {}".format(tNoti))
                break
            else:
                time.sleep(0.001)

    #check version
    version_num = 'version: ' + JcSmartDevicePyd.SI_PyGetVersion()
    print("version", version_num)
    waitForReply()
    #
    #uninitialize
    # nRet = JcSmartDevicePyd.SI_PyUninit(sDevSN)

    # initialize
    nRet = JcSmartDevicePyd.SI_PyInit(sDevSN)
    print('init', nRet)
    waitForReply()

    #set exposure time
    tParam = JcSmartDevicePyd.JcSetExpGainParam()
    tParam.m_nExp = 5500
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_EXPGAIN_VALUE,tParam)
    print("set Exposure Time", nRet)
    waitForReply()

    # TODO: set aperture to "clear"
    # tParamMain = JcSmartDevicePyd.JcMainFlowParam()
    #

    #take picture
    tParamSNAP = JcSmartDevicePyd.JcSetExpGainParam()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE,tParamSNAP)
    print("take picture", nRet)
    waitForReply()

    #開始測量
    tParamMes = JcSmartDevicePyd.JcMeasure()
    # tParamMes.m_nPtnNo = self.sbPattenNo.value()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_MEASURE_OPERATE,tParamMes)
    print("start measure", nRet)
    waitForReply()


