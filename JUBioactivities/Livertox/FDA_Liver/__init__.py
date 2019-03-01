import os.path, glob
import pandas as pd
from ... import utils


__data_src__ = glob.glob(os.path.join(__path__[0], "*.sdf"))


def read_data(raw=False):
    keys = ['Composite Activity - Score','Alkalkine Phosphatase Increase - Activity Score',
                     'SGOT Increase - Activity Score', 'SGPT Increase - Activity Score','LDH Increase - Activity Score',
                     'GGT Increase - Activity Score']
    names = ['Composite_DILI_FDA', 'Alkalkine_Phosphatase_Increase_FDA',
                     'SGOT_Increase_FDA', 'SGPT_Increase_FDA', 'LDH_Increase_FDA',
                     'GGTIncrease_FDA']
    df = utils.read_labelled_molecules(__data_src__[0], key=keys, name=names)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.convert_to_classes(df, 'A', 'I')
    df = utils.handle_duplicates(df, type='bin')
    return df

def read_structures(raw=False):
    df = utils.read_labelled_molecules(__data_src__[0], key='Activity', structures=True)

    if raw:
        return df

    df = utils.drop_rows(df)
    df = utils.handle_duplicates(df, type='str')
    return df

