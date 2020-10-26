import os
import sys
import datetime
import time
import re
import pandas as pd
import pandasdmx
from plotnine import ggplot
import matplotlib as mpl
import matplotlib.pyplot as plt
print("Python version= {0}".format(sys.version_info))
print("Pandas version= {0}".format(pd.__version__))
print("Datetime= {0}".format(datetime.datetime.now()))

oecd = pandasdmx.Request('OECD')
metadata = oecd.datastructure('DSD_une_rt_a')

In [4]: metadata

data_response = oecd.data(resource_id='MEI_CLI', key={'GEO':'US'}, dry_run=True) # #key='all?startTime=2018')
data_response