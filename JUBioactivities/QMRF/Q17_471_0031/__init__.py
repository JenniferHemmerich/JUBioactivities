import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))

def _read_d(file, raw=False):
    keys = ["OVERALL","TA100","TA100_S9","TA1535","TA1535_S9","TA97","TA97_S9","TA1538","TA1538_S9","TA98","TA98_S9",
            "TA1537","TA1537_S9","TA102","TA102_S9","TA104","TA104_S9","TA98(NR)","TA98(NR)_S9","TA97A","TA97A_S9",
            "TA98(1,8-DNP6)","TA98(1,8-DNP6)_S9","TA100(1,8-DNP6)","TA100(1,8-DNP6)_S9","TA100(NR)","TA100(NR)_S9",
            "YG1024","YG1024_S9","TA2638","TA2638_S9","YG1029","YG1029_S9","TA92","TA92_S9","YG1026","YG1026_S9","YG1021",
            "YG1021_S9","TA7004","TA7004_S9","TA7005","TA7005_S9","TA1978","TA1978_S9","TA7002","TA7002_S9","TA7003",
            "TA7003_S9","TA7001","TA7001_S9","TA7006","TA7006_S9","TM677","TM677_S9","G46","G46_S9","YG1020","YG1020_S9",
            "YG1025","YG1025_S9","TA94","TA94_S9"]
    cols = ["OVERALL_Ames_Q17_471_0031","TA100_Ames_Q17_471_0031","TA100_S9_Ames_Q17_471_0031","TA1535_Ames_Q17_471_0031",
            "TA1535_S9_Ames_Q17_471_0031","TA97_Ames_Q17_471_0031","TA97_S9_Ames_Q17_471_0031","TA1538_Ames_Q17_471_0031",
            "TA1538_S9_Ames_Q17_471_0031","TA98_Ames_Q17_471_0031","TA98_S9_Ames_Q17_471_0031","TA1537_Ames_Q17_471_0031",
            "TA1537_S9_Ames_Q17_471_0031","TA102_Ames_Q17_471_0031","TA102_S9_Ames_Q17_471_0031","TA104_Ames_Q17_471_0031",
            "TA104_S9_Ames_Q17_471_0031","TA98(NR)_Ames_Q17_471_0031","TA98(NR)_S9_Ames_Q17_471_0031","TA97A_Ames_Q17_471_0031",
            "TA97A_S9_Ames_Q17_471_0031","TA98(1,8-DNP6)_Ames_Q17_471_0031","TA98(1,8-DNP6)_S9_Ames_Q17_471_0031",
            "TA100(1,8-DNP6)_Ames_Q17_471_0031","TA100(1,8-DNP6)_S9_Ames_Q17_471_0031","TA100(NR)_Ames_Q17_471_0031",
            "TA100(NR)_S9_Ames_Q17_471_0031","YG1024_Ames_Q17_471_0031","YG1024_S9_Ames_Q17_471_0031","TA2638_Ames_Q17_471_0031",
            "TA2638_S9_Ames_Q17_471_0031","YG1029_Ames_Q17_471_0031","YG1029_S9_Ames_Q17_471_0031","TA92_Ames_Q17_471_0031",
            "TA92_S9_Ames_Q17_471_0031","YG1026_Ames_Q17_471_0031","YG1026_S9_Ames_Q17_471_0031","YG1021_Ames_Q17_471_0031",
            "YG1021_S9_Ames_Q17_471_0031","TA7004_Ames_Q17_471_0031","TA7004_S9_Ames_Q17_471_0031","TA7005_Ames_Q17_471_0031",
            "TA7005_S9_Ames_Q17_471_0031","TA1978_Ames_Q17_471_0031","TA1978_S9_Ames_Q17_471_0031","TA7002_Ames_Q17_471_0031",
            "TA7002_S9_Ames_Q17_471_0031","TA7003_Ames_Q17_471_0031","TA7003_S9_Ames_Q17_471_0031","TA7001_Ames_Q17_471_0031",
            "TA7001_S9_Ames_Q17_471_0031","TA7006_Ames_Q17_471_0031","TA7006_S9_Ames_Q17_471_0031","TM677_Ames_Q17_471_0031",
            "TM677_S9_Ames_Q17_471_0031","G46_Ames_Q17_471_0031","G46_S9_Ames_Q17_471_0031","YG1020_Ames_Q17_471_0031",
            "YG1020_S9_Ames_Q17_471_0031","YG1025_Ames_Q17_471_0031","YG1025_S9_Ames_Q17_471_0031","TA94_Ames_Q17_471_0031",
            "TA94_S9_Ames_Q17_471_0031"]
    df = utils.read_labelled_molecules(file, key=keys, name=cols)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, pos='3', neg='1')
    df = utils.handle_duplicates(df, type='bin')
    return df

def _read_s(file, raw=False):
    df = utils.read_labelled_molecules(file, key='', name='Ames_Q17_416_0041', structures=True)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df


def read_data(raw=False):
    df = pd.concat([_read_d(f,raw) for f in __data_src__], axis=1)
    if raw:
        return df
    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='bin')

    return df

def read_structures(raw=False):
    df = pd.concat([_read_s(f,raw) for f in __data_src__])
    if raw:
        return df
    df= utils.handle_duplicates(df, type='str')
    return df
