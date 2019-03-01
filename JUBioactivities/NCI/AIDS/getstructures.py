import cirpy
import pandas as pd
from urllib.error import HTTPError

structures = []
inchis = []
casnos = pd.read_csv("NSC_CAS_Sept2013.csv", index_col=0, names=['NSC','CAS'])


for index, cas in casnos.iterrows():
    print(index,cas['CAS'])
    try:
        structures.append(cirpy.resolve(cas['CAS'],'smiles'))
    except HTTPError:
        structures.append('not found')
    try:
        inchis.append(cirpy.resolve(cas['CAS'],'stdinchi'))
    except HTTPError:
        inchis.append('not found')

casnos['Inchi'] = inchis
casnos['Smiles'] = structures

casnos.to_csv('Structures.csv')