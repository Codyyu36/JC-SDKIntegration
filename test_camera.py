import JcSmartDevicePyd

vecDevList = JcSmartDevicePyd.SI_PyGetDeviceList()
nDevCnt = len(vecDevList)

if nDevCnt < 1:
    print('No device find.')
else:
    sDevSN = "61CF-02"  # 设备 SN

    #initialize
    nRet = JcSmartDevicePyd.SI_PyInit(sDevSN)
    print('init', nRet)

    #get device info
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_GET_DEVICE_INFO)
    print('eREQ_GET_DEVICE_INFO', nRet)

    #set exposure time
    tParam = JcSmartDevicePyd.JcSetExpGainParam()
    tParam.m_nExp = 5500
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_EXPGAIN_VALUE,tParam)
    print('eREQ_SET_EXPGAIN_VALUE', nRet)

    # TODO: set aperture to "clear"
    # tParamMain = JcSmartDevicePyd.JcMainFlowParam()
    #

    #take picture
    tParamSNAP = JcSmartDevicePyd.JcSetExpGainParam()
    nRet = JcSmartDevicePyd.SI_PyOperations(sDevSN,JcSmartDevicePyd.eREQ_SET_SNAP_OPERATE,tParamSNAP)
    print('eREQ_SET_SNAP_OPERATE', nRet)
