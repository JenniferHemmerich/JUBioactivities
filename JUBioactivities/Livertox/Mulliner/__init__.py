import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))


def read_data(raw=False):
    keys = ["H_HT_class",
            "H_CC_class",
            "H_MF_class",
            "H_MFHB_class",
            "H_MFHC_class",
            "PC_HT_class",
            "PC_CC_class",
            "PC_MF_class",
            "PC_CCHB_class",
            "PC_CCHC_class",
            "PC_MFHB_class",
            "PC_MFHC_class",
            "PC_HTdl500_class",
            "PC_CCdl500_class",
            "PC_MFdl500_class",
            "PC_CCHCdl500_class",
            "PC_CCHBdl500_class",
            "PC_MFHCdl500_class",
            "PC_MFHBdl500_class",
            "H_CCHB_class",
            "H_CCHC_class"]
    names = ["H_HT_Mulliner",
             "H_CC_Mulliner",
             "H_MF_Mulliner",
             "H_MFHB_Mulliner",
             "H_MFHC_Mulliner",
             "PC_HT_Mulliner",
             "PC_CC_Mulliner",
             "PC_MF_Mulliner",
             "PC_CCHB_Mulliner",
             "PC_CCHC_Mulliner",
             "PC_MFHB_Mulliner",
             "PC_MFHC_Mulliner",
             "PC_HTdl500_Mulliner",
             "PC_CCdl500_Mulliner",
             "PC_MFdl500_Mulliner",
             "PC_CCHCdl500_Mulliner",
             "PC_CCHBdl500_Mulliner",
             "PC_MFHCdl500_Mulliner",
             "PC_MFHBdl500_Mulliner",
             "H_CCHB_Mulliner",
             "H_CCHC_Mulliner"]
    df = utils.read_labelled_molecules(__data_src__[0], key=keys, name=names)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = utils.handle_duplicates(df, type='bin')
    return df


def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='Activity', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

