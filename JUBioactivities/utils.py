import os, sys
import contextlib

import numbers
import pandas
import numpy 
from rdkit import Chem
from standardiser import standardise
from standardiser.utils import StandardiseException
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


@contextlib.contextmanager
def redirect(stream, drain):
    """ Context manager to redirect streams on file-descriptor level. """
    fd = stream.fileno()

    with os.fdopen(os.dup(fd), 'wb') as stream_copy:
        stream.flush()
        os.dup2(drain.fileno(), fd)

        try:
            yield stream
        finally:
            stream.flush()
            os.dup2(stream_copy.fileno(), fd)


def silence(stream):
    """ Decorator to suppress a stream. """
    if isinstance(stream, str):
        stream = getattr(sys, stream)

    def silence_decorator(func):
        def silence_func(*args, **kwargs):
            with open(os.devnull, 'w') as drain:
                with redirect(stream, drain):
                    return func(*args, **kwargs)

        return silence_func
    return silence_decorator


#@silence('stderr')
def convert_index(index, filenames=False):
    """
    Convert the index of a pandas DataFrame to an InchiKey.

    Parameters
    ----------
    index : pandas.Index
        The index of the dataframe to be converted.
    filenames : bool, optional
        Flag to indicate that the index consists of filenames
        rather than direct representations. Defaults to `False`.

    Returns
    -------
    index : pandas.Index
        An index where each element has been translated to its inchikey.

    Notes
    -----
    OpenBabel tends to print quite a bit of warnings,
    which can be considered irrelevant (apparently).
    The @silence decorator allows to suppress this output.
    This might, however, also mask more severe errors!
    """
    if not isinstance(index, pandas.Index):
        index = pandas.Index(index)

    # choose the correct read function
    if filenames and index.nunique() < len(index):
        cache = {}

        def read_mol(f):
            it = cache.setdefault(f,Chem.SDMolSupplier(f))
            try:
                return next(it)
            except StopIteration:
                raise ValueError("More indices than molecules in file '{}'".format(f))
    else:
        def read_mol(fname):
            if not filenames:
                return Chem.MolFromSmiles(fname)
            else:
                return next(Chem.SDMolSupplier(fname))

    def _convert(fname):
        """ read molecule from file and convert to inchikey. """

        mol = read_mol(fname)

        if mol is not None:
            try:
                mol = standardise.run(mol)
            except StandardiseException:
                mol = mol
            mol = Chem.MolToInchi(mol)
            mol = Chem.InchiToInchiKey(mol)
            return mol.rstrip()
        else:
            return("could not read molecule from '{}'".format(fname))

    # fix index
    index = index.map(_convert)
    index.name = 'InchiKey'

    return index


#@silence('stderr')
def read_labelled_molecules(filename, key, name=None, structures=False):
    """
    Read molecules with corresponding labels in the same file into a DataFrame.

    Parameters
    ----------
    filename : str
        The filename to read from.
    key : str or list
        The key(s) under which the labels are stored.
    name : str,list or None, optional
        The column name(s) for the collected key.
        If `None`, the filename is used as key-name.
    structures: bool
        If Inchi keys along with structures should be returned. If True it
        will ignore key and names and return a dataframe with InchiKeys as Index
         and a column 'Smiles' containing generated SMILES strings

    Returns
    -------
    df : pandas:dataFrame
        The dataframe that has been created from the data in the files
        with inchikeys as indices.

    Notes
    -----
    if key and name are lists they have to be the same length,
    otherwise an assertion error will be raised


    OpenBabel tends to print quite a bit of warnings,
    which can be considered irrelevant (apparently).
    The @silence decorator allows to suppress this output.
    This might, however, also mask more severe errors!
    """


    if type(name) is list and type(key) is list:
        assert len(name) == len(key)

    else:
        if name is None:
            fname_clean = os.path.basename(filename)
            name = os.path.splitext(fname_clean)[0]
        name = [name]
        key = [key]

    # collect data
    mols = [mol for mol in Chem.SDMolSupplier(filename)]

    def _getdata(mol, key):
        if mol is not None:
            try:
                return mol.GetProp(key)
            except KeyError:
                return numpy.nan
        else:
            return numpy.nan

    def _convert(mol):
        """ standardise Molecule and convert to inchikey. """
        if mol is not None:
            try:
                mol = standardise.run(mol)
            except StandardiseException:
                mol = mol
            mol = Chem.MolToInchi(mol)
            mol = Chem.InchiToInchiKey(mol)
            if mol is None:
                return ("could not generate_InchiKey")
            else:
                return mol.rstrip()
        else:
            return("could not read molecule")
    

    ids = [_convert(mol).rstrip() for mol in mols]

    def _convert_SMILES(mol):
        """ Convert given RDKit Molecule if it is not None to Smiles"""
        if mol is None:
            return None
        else:
            return Chem.MolToSmiles(mol)

    # create dataframe
    if structures:
        # Get SMILES according to read structures
        struc = [_convert_SMILES(mol) for mol in mols]
        df = pandas.DataFrame({'Smiles':struc},index=ids) #return structures and Inchi
        return df
    else:
        # collect data based on keys
        data = dict()

        for n, k in zip(name, key):
            data[n] = [_getdata(mol, k) for mol in mols]

        df = pandas.DataFrame(data, index=ids)
        df.index.name = 'InchiKey'
        return df


def print_duplicates(data, inchi_index=None):
    """
    Print the duplicate inchikeys and their values.

    Parameters
    ----------
    data : pandas.DataFrame
        The dataframe before changing the keys to inchi.
    inchi_index : pandas.Index or None
        The index object containing the inchikeys.
        If `None`, it is assumed that `data` has inchikeys as indices.
    """
    index = data.index if inchi_index is None else inchi_index

    is_dup = index.duplicated(False)
    data = data[is_dup]

    if inchi_index is not None:
        data.index = data.index.map(os.path.basename)
        data.reset_index(inplace=True)
        data.index = inchi_index[is_dup]

    print(data.sort_index())
    print(numpy.where(is_dup))

def drop_rows(data, lookup = 'could not'):
    """
    Remove molecules with a specific index.
    Lookup defaults to 'could not read molecule' as
    failed molecules have the index 'could not read molecule'
    
    Parameters
    ----------
    data : pandas.DataFrame
        The dataframe after changing the keys to inchi.
    lookup : str
        The index of rows which should be dropped, defaults to 'could not read molecule'
    exact : bool
        True, if the lookup string should be an exact match to the index value


    Returns
    -------
    data : pandas.DataFrame
        a dataframe with dropped rows as given by lookup
    """

    broken = data.index.str.contains(lookup)
    data = data[broken == False]
    loc_broken = numpy.where(broken)
    print("Dropped '{}' molecules at rows '{}'".format(len(loc_broken), str(loc_broken[0]))) #TODO give out useful values

    return data

def handle_duplicates(data, type):
    """
        Handles duplicate molecules. Assumes that dataframe has InChI Keys as values
        Checks if duplicates have the same activity value:
        If  True: keep one copy
            False: remove molecule

        Parameters
        ----------
        data : pandas.DataFrame
            The dataframe after changing the keys to inchi.
        type : str
               'bin' for binary data,
               'cont' for continouus data
               'mult' for Multi-group data
               'str' for String data


            Whether data is continouus, binary or else, if 'cont' it is assumed that the data is continouus,
            hence values will be averaged, if values are binary or multigroup a majority vote will be cast,
            compounds with disagreeing labels (eg a tie in the vote) will be discarded,
            for strings only the first found string will be kept

        Returns
        -------
        no_dups : pd.DataFrame
            a dataframe with handled duplicates
            For continues averaged values,
            for binary or multiclass activities/values majority vote (ties are removed)
            for others same as for binary values

        """
    if type not in ['cont','mult','bin','str']:
        print('Could not handle duplicates. Please enter valid str for parameter type \n'
              'Options are bin, cont, mult, str \n but found',type
              )
        raise ValueError

    if type == 'cont':
        no_dups = data.groupby(data.index).mean()
        return no_dups

    if type == 'bin':
        # replace values per majority vote
        # If majority is 0 or 1 -> median will be as well , else 0.5
        # for ties, eg value is 0.5 => drop molecule
        no_dups = data.groupby(data.index).median()

        # remove conflicting values
        no_dups = no_dups.replace(0.5, numpy.nan)

        return no_dups

    if type == 'mult':
        grouped = data.groupby(data.index)
        no_dups = grouped.aggregate(lambda x: list(x))

        def _getactivity(x):
            """
            For multi-class labels activity is determined by majority vote

            Parameters
            ----------
            x : pandas.Series
                row of Pandas dataframe
            Returns
            -------
            x or None
                 x if it is a single value
                 majority class if it can be determined
                 None if majority class cannot be determined (no value which fulfills count(value)> no of values/2
            """

            elem = len(x)
            values, counts = numpy.unique(x, return_counts=True)
            activity, = numpy.where(counts > elem/2)
            if len(values) == 1:
                return values[0]
            elif len(activity) == 1:
                return values[activity[0]]
            else:
                return None


        no_dups = no_dups.applymap(_getactivity)
        no_dups = no_dups.dropna()
        return no_dups

    if type == 'str':
        no_dups = data.groupby(data.index).first()
        return no_dups

def convert_to_classes(data,pos,neg):
    """
    Converts a DataFrame with str or numeric labels to binary labels. Returned dataframe has positive
    labels encoded as 1, negatives as 0

    Parameters
    ----------
    data: pandas.Dataframe
        Dataframe where labels need to be converted to binary classes

    pos: str, int
        label for positive class, if numbers are Strings in the dataframe
        they have to be passed as strings

    neg: str,int
        label for negative class, if numbers are Strings in the dataframe
        they have to be passed as strings

    Returns
    -------
    df: pandas.DataFrame
        dataframe with the binary class labels positive labels are encoded as 1, negatives as 0
    """

    allowed_vals = [pos, neg]
    data[~data.isin(allowed_vals)] = numpy.nan
    data.replace(allowed_vals, value=[1, 0], inplace=True)
    return data

def one_hot_encode(data,cols):
    """
    Parameters
    ----------
    data: pandas.DataFrame
        dataframe with at least one multiclass column to be one-hot encoded

    col: list
        list of colums to be iterated over to do one hot encoding
        Fails with assertion error if col is not a list

    Returns
    -------
    df: pandas.DataFrame
        dataframe with one column containing the one-hot encoded labels as a list.
    """

    assert isinstance(cols,list)
    for col in cols:
        #Encode as labels
        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(data[col])

        # binary encode
        onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1) #onehot expects 2D array
        onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
        onehot_encoded = pandas.DataFrame(onehot_encoded)
        vals = onehot_encoded.values.tolist()
        data[col] = vals

    return data

#@silence('stderr')
def get_smiles_from_index(df, filenames=True):
    """
    Convert the index with Smiles or filenames of a pandas DataFrame
    to a Smiles column with rdkit compliant SMILES.

    Parameters
    ----------
    index : pandas.DataFrame
        The dataframe with the index to be converted.

    filenames : bool, optional
        Flag to indicate that the index consists of filenames
        rather than direct representations. Defaults to `False`.

    Returns
    -------
    df pandas.DataFrame
        Dataframe with additional column Smiles generated from Index files.

    Notes
    -----
    OpenBabel tends to print quite a bit of warnings,
    which can be considered irrelevant (apparently).
    The @silence decorator allows to suppress this output.
    This might, however, also mask more severe errors!
    """
    inchi_index = df.index

    # choose the correct read function
    if filenames and inchi_index.nunique() < len(inchi_index):
        cache = {}

        def read_mol(f):
            it = cache.setdefault(f,Chem.SDMolSupplier(f))
            try:
                return next(it)
            except StopIteration:
                raise ValueError("More indices than molecules in file '{}'".format(f))
    else:
        def read_mol(fname):
            if not filenames:
                return Chem.MolFromSmiles(fname)
            else:
                return next(Chem.SDMolSupplier(fname))

    def _convert(fname):
        """ read molecule from file and convert to inchikey. """

        mol = read_mol(fname)

        if mol is not None:
            mol = Chem.MolToSmiles(mol)
            return mol.rstrip()
        else:
            return("could not read molecule from '{}'".format(fname))

    df['Smiles'] = inchi_index.map(_convert).values

    return df

#@silence('stderr')
def index_from_inchicode(df, smiles = False):
    """
    Create a dataframe with InchiKeys as index from a dataframe containing Inchicodes as Index
    if smiles is true the returned dataframe contains a new column calles Smiles containing
    the generated smiles strings from the inchicodes

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the innchi-code index to be converted.

    smiles : bool, optional
        Flag to indicate if the returned dataframe should contain a Column with the SMILES
        values generated from the inchicodes

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with InchiKeys as index and additional column Smiles generated from Index files if smiles was set True.

    Notes
    -----
    OpenBabel tends to print quite a bit of warnings,
    which can be considered irrelevant (apparently).
    The @silence decorator allows to suppress this output.
    This might, however, also mask more severe errors!
    """

    keys = []
    for f in df.index.values:
        try:
            keys.append(Chem.InchiToInchiKey(f))
        except:
            keys.append(None)

    if smiles:
        smi = []
        for m in df.index.values:
            if not pandas.isnull(m): # m could be nan or None
                mol = Chem.MolFromInchi(m)

                if mol is not None:
                    mol = Chem.MolToSmiles(mol)
                else:
                    mol = ''.join(['Could not read molecule from', str(m)])
            else:
                mol = ''.join(['Could not read molecule from', str(m)])
            smi.append(mol)
        df['Smiles'] = smi
        df.index = pandas.Index(keys)
        return df
    else:
        df.index = pandas.Index(keys)
        return df[df.index.notnull()]









