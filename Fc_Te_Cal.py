import numpy as np
import pandas as pd
#np.seterr(divide='ignore',invalid='ignore')

def FcTeCal(Vmtx, Amtx, step):
    RC_mtx = [[[-0.679439, 0.135273, 0.015946, -0.001189],
               [0.029665, 0.004808, -0.000020535, 0.000000055409285],
               [-0.000276, 0.000083329, 0.000000937, -0.00000002479644],
               [0.000001487, -0.000061321, 0.000000304, -0.000000004467234]],
              [[0.887447, 0.148841, 0.03055, -0.001348],
               [0.070994, 0.00387, 0.000093228, -0.000000706],
               [-0.000786, -0.000926, 0.000049181, -0.000000314],
               [0.000004616, 0.000046144, -0.00000141, 0.0000000081724008]],
              [[-0.728042, 0.012211, 0.023371, -0.000093243],
               [0.02495, 0.010145, -0.000103, 0.000000618],
               [-0.000205, -0.000549, 0.000037592, -0.000000213],
               [0.000001949, -0.000113, 0.00000331, -0.00000001739372]],
              [[-1.067682, 0.254363, 0.008866, -0.000951],
               [0.046423, 0.015482, -0.000131, 0.000000328],
               [-0.000173, 0.002876, -0.00005866, 0.00000024],
               [0.000000569, -0.000321, 0.000001943, -0.00000001257413]]]
    RC_mtx = np.array(RC_mtx)
    Vmtx = np.array(Vmtx)/100
    Amtx = np.abs(np.array(Amtx)/100)
    reslist = np.array([0.0, 0.0, 0.0, 0.0])

    for k in range(4):
        MOE = 0
        RC = RC_mtx[k]
        for i in range(4):
            for j in range(4):
                moe = (np.sum(RC[i][j] * (Vmtx**i) * (Amtx**j) * step, axis=0)).mean()/400
                MOE = MOE + moe
        reslist[k] = np.exp(MOE)
    return reslist

def NFR_cal(vsp):
    if vsp > 0:
        return 1.71 * (vsp**0.42) * 0.1
    else:
        return 1 * 0.1


def FMCal_VSP(Vmtx, Amtx, step):
    Vmtx = np.array(Vmtx) / 100.0
    Amtx = np.array(Amtx) / 100.0
    VSP = Vmtx * (1.1*Amtx + 0.132) + 0.000302*(Vmtx**3)
    NFR = np.vectorize(NFR_cal)(VSP)
    avgNFR = NFR.mean()*10
    return avgNFR

def EMCal_CO(Vmtx, Amtx, step):
    Vmtx = np.array(Vmtx) / 100.0
    Amtx = np.array(Amtx) / 100.0

    f1 = 0.553; f2 = 0.16; f3 = -0.00289; f4 = 0.266; f5 = 0.511; f6 = 0.183
    em = f1 + f2*Vmtx + f3*(Vmtx**2) + f4*Amtx + f5*(Amtx**2) + f6*Vmtx*Amtx
    EM = np.maximum(em*step, np.zeros(em.shape))
    EM_cal = EM.mean()*10
    return EM_cal

def EMCal_NO(Vmtx, Amtx, step):
    Vmtx = np.array(Vmtx) / 100.0
    Amtx = np.array(Amtx) / 100.0

    f = Amtx.copy()
    f1 = np.where(f >= -0.5, 0.000619, 0.000217)
    f2 = np.where(f >= -0.5, 0.00008, 0.0)
    f3 = np.where(f >= -0.5, -0.00000403, 0.0)
    f4 = np.where(f >= -0.5, -0.000413, 0.0)
    f5 = np.where(f >= -0.5, 0.00038, 0.0)
    f6 = np.where(f >= -0.5, 0.000177, 0.0)

    em = f1 + f2*Vmtx + f3*(Vmtx**2) + f4*Amtx + f5*(Amtx**2) + f6*Vmtx*Amtx
    EM = np.maximum(em*step, np.zeros(em.shape))
    EM_cal = EM.mean()*10
    return EM_cal


def EMCal_VOC(Vmtx, Amtx, step):
    Vmtx = np.array(Vmtx) / 100.0
    Amtx = np.array(Amtx) / 100.0

    f = Amtx.copy()
    f1 = np.where(f >= -0.5, 0.000447, 0.00263)
    f2 = np.where(f >= -0.5, 0.000000732, 0.0)
    f3 = np.where(f >= -0.5, -0.0000000287, 0.0)
    f4 = np.where(f >= -0.5, -0.00000341, 0.0)
    f5 = np.where(f >= -0.5, 0.00000494, 0.0)
    f6 = np.where(f >= -0.5, 0.00000166, 0.0)

    em = f1 + f2*Vmtx + f3*(Vmtx**2) + f4*Amtx + f5*(Amtx**2) + f6*Vmtx*Amtx
    EM = np.maximum(em*step, np.zeros(em.shape))
    EM_cal = EM.mean()*10
    return EM_cal

def EMCal_PM(Vmtx, Amtx, step):
    Vmtx = np.array(Vmtx) / 100.0
    Amtx = np.array(Amtx) / 100.0

    f1 = 0.0; f2 = 0.0000157; f3 = -0.000000921; f4 = 0.0; f5 = 0.0000375; f6 = 0.0000189
    em = f1 + f2*Vmtx + f3*(Vmtx**2) + f4*Amtx + f5*(Amtx**2) + f6*Vmtx*Amtx
    EM = np.maximum(em*step, np.zeros(em.shape))
    EM_cal = EM.mean()*10
    return EM_cal