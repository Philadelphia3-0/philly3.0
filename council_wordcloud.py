# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 13:43:21 2015

@author: zoeydavidson
"""

import numpy as np
import wordcloud as wc #https://amueller.github.io/word_cloud/index.html
import matplotlib.pyplot as plt
import pandas as pd
from scipy.misc import imread
from backend import filter_amends

dataroot = '/Users/zoeydavidson/Documents/Code/philly3.0/data/' #fill me in
csv_dtype = {'EntityZip' : str,
             'EmployerZip': str}

ytd20151027 = pd.read_csv(dataroot+'Explorer.Transactions.2015.YTD_2015-10-27.csv',sep='\t',quotechar='"',error_bad_lines=False, dtype=csv_dtype)
ftags = pd.read_csv(dataroot+'filer_tags.csv')
councilfilers = ftags[ftags['Office Sought']=='City Council']
fytd20151027 = ytd20151027.iloc[filter_amends(ytd20151027)]
ccfinances = fytd20151027[fytd20151027.FilerName.isin(councilfilers.Filers.values)]
ccfinances2 = ccfinances.loc[ccfinances.Cycle==2]
description_words = ccfinances2.loc[ccfinances2['DocType']=='CFR - Schedule III - Statement of Expenditures']['Description'].dropna().to_string()
description_words = description_words.replace('\n',' ')

phillymask = imread(dataroot+"images/philly_mask_8bit.png").astype(int)
awc = wc.WordCloud(background_color='white', max_words=200, mask=phillymask)
wcim = awc.generate(description_words)
poutline = imread(dataroot+'images/Philly_outline.png')
wcarr = wcim.to_array()
combined_arr = wcarr + np.abs(poutline-255)

plt.figure(figsize=(32,24))
plt.imshow(combined_arr)
plt.axis("off")