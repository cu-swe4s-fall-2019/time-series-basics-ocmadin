# time-series-basics
This code takes some data from the folder `smallData`, in the form of csvs, cleans it, and produces output csvs based on rounded times.

Usage: `python data_import.py --folder_name smallData/ --output_file 5out.csv --sort_key smallData/cgm_small.csv`
## Pandas

This is an improved version of the previous problem that uses `pandas` to solve the problem.
Usage: `python pandas_import.py`

This file takes all the csv files that are in the `smallData` folder, puts them all into pandas dataframes, then strips non-numerical values.  These dataframes are then joined based on the time index for `cgm_small`.  Then, the times are rounded and `groupby` is used to add or average each value accordingly.  It then outputs these to csv files.

## Benchmarking

The benchmarks and results are as follows:

### Original
``` /usr/bin/time -f '%e\t%M' python data_import.py --folder_name smallData/ --output_file 5out.csv --sort_key 
11.21	50468

```

### Pandas
``` /usr/bin/time -f '%e\t%M' python pandas_import.py 
2.47	103060
```

This new version with pandas performs much better!

