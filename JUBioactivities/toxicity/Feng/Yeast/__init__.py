import os.path
import pandas as pd
import numpy
from .... import utils


__data_src__ = [os.path.join(__path__[0], x) for x in ["yeast_all_w_activity.sdf"]]


def read_data(raw=False):
    keys = ["AVEINH_bub3_Yeast_Feng", "AVEINH_cln2_rad14_Yeast_Feng", "AVEINH_mec2-1_Yeast_Feng",
                                                        "AVEINH_mlh1_Yeast_Feng", "AVEINH_rad18_Yeast_Feng"]
    names = ["AVEINH_bub3_Yeast_Feng", "AVEINH_cln2_rad14_Yeast_Feng", "AVEINH_mec2-1_Yeast_Feng",
                                                        "AVEINH_mlh1_Yeast_Feng", "AVEINH_rad18_Yeast_Feng"]
    df = utils.read_labelled_molecules(__data_src__[0], key=keys, name=names)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = df.apply(pd.to_numeric)
    df = df.replace(9999, numpy.nan)
    df = utils.handle_duplicates(df, type='cont')
    return df

def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='EXTREG', name='Name', structures=True)
    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df