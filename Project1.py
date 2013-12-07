# First commands with Python

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import json 

# Data usa.gov
path = 'usagov_bitly_data2013-05-17-1368832207'

records = [json.loads(line) for line in open(path)]

print('Example record')
print records[0]

print('')
print('Example timezone field in records[0]')
print records[0]['tz']

time_zones = [rec['tz'] for rec in records if 'tz' in rec]

print('')
print('First 10 time zones')
print time_zones[:10]

# Counting time zones with pandas
frame = DataFrame(records)

tz_counts = frame['tz'].value_counts()
print tz_counts[:10]

# Clean empty/na fields
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'

# Re-counting tz fields
print('')
tz_counts = clean_tz.value_counts() 
print tz_counts[:10]

# Plot 10 First most common tz
print tz_counts[:10].plot(kind='barh', rot=0)

# Split Windows/Not Windows OS
cframe = frame[frame.a.notnull()]

operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')

# Print List of the first 5
operating_system[:5]

# Group by tz column & OS
by_tz_os = cframe.groupby(['tz', operating_system])

agg_counts = by_tz_os.size().unstack().fillna(0)
print('')
print('LIST by OS')
print agg_counts[:10]

# Bar Plot
indexer = agg_counts.sum(1).argsort()

count_subset = agg_counts.take(indexer)[-10:]
count_subset.plot(kind='barh', stacked=True) 
