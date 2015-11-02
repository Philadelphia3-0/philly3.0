# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:04:14 2015
Basic filtering operations for analyzing aggregate YTD campaign transactions
Data can be found at
ftp://ftp.phila-records.com/Year-to-Date Transaction Files/
@author: zoeydavidson
"""

import numpy as np
import pandas as pd


def filter_amends(df):
    """
    df is a ytd data frame including amended reports.
    This function filters out duplicate information in amendment stages and 
    keeps only the latest data.
    Pseudocode:
        -for each cycle check for each filer check if amended records
            -if filer in cycle had an amended record get most recent subdate:
                keep those lines
            -if filer had no amendments in cycle keep those lines
    returns a list of indices of lines in dataframe corresponding to latest
    filing data
    """
    indices_to_keep = np.array([],dtype='int64')
    cycles = df.Cycle.unique()
    for c in cycles:
        filers = df.loc[df.Cycle==c].FilerName.unique()
        dfc = df.loc[df.Cycle==c]
        for f in filers:
            dfcf = dfc.loc[dfc.FilerName==f]
            if np.sum(dfcf.Amended.str.contains('Y|y',na=False)):
                #print "amended: " + str(dfcf.SubDate.max())
                maxdate = dfcf.SubDate.max()
                #print 'amended: '+str(dfcf.loc[dfcf.SubDate == maxdate].index)
                indices_to_keep=np.append(indices_to_keep,dfcf.loc[dfcf.SubDate == maxdate].index)
            else:
                #print "not amended"
                indices_to_keep=np.append(indices_to_keep,dfcf.index)
    return indices_to_keep

