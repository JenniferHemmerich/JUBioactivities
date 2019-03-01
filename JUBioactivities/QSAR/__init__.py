import pandas as pd

from .aquatox import read_data as read_aquatox
from .artemisin import read_data as read_artemisin
from .bioconcentration import read_data as read_biocon
from .biodegradation import read_data as read_biodeg
from .cytochromeP450 import read_data as read_cytochrome
from .fishtox import read_data as read_fishtox
from .neighbourhood import read_data as read_neighbour
from .steroid import read_data as read_steroid
from .sutherland import read_data as read_suth
from .sutherland4 import read_data as read_suth4
from .SXRligand import read_data as read_sxr


def read_data():
    df = pd.concat([
        read_aquatox(),
        read_artemisin(),
        read_biocon(),
        read_biodeg(),
        read_fishtox(),
        read_neighbour(),
        read_steroid(),
        read_suth(),
        read_suth4(),
        read_sxr()
    ], axis=1)

    # assure that column names are unique
    assert df.columns.nunique() == len(df.columns)
    return df
