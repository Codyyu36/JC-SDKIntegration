import JcSmartDevicePyd
import time

vecDevList = JcSmartDevicePyd.SI_PyGetDeviceList()
nDevCnt = len(vecDevList)

if nDevCnt < 1:
    print('No device find.')
else:
    sDevSN = "FW151A001" # 设备 SN

    #check version
    version_num = 'version: ' + JcSmartDevicePyd.SI_PyGetVersion()
    print("version", version_num)
    #
    #uninitialize
    # nRet = JcSmartDevicePyd.SI_PyUninit(sDevSN)

    # initialize
    nRet = JcSmartDevicePyd.SI_PyInit(sDevSN)
    print('init', nRet)
    time.sleep(20)

    #set exposure time
    tParam = JcSmartDevicePyd.JcSetExpGainParam()
    tParam.m_nExp = 5500
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_EXPGAIN_VALUE,tParam)
    print("set Exposure Time", nRet)
    time.sleep(3)
    # TODO: set aperture to "clear"
    # tParamMain = JcSmartDevicePyd.JcMainFlowParam()
    #

    #take picture
    tParamSNAP = JcSmartDevicePyd.JcSetExpGainParam()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE,tParamSNAP)
    print("take picture", nRet)
    #analyze and save picture

