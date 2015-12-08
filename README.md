This is a python script that takes in one paramter which represetns the column name and two .csv files which 
are predfined inside the script and performs certain comparisons and generates a new file. The scripts utlizes these
libraries/packages below:
 1. pandas
 2.collections
 3.functools
 4.math
 5.optparse

If these pacakges are not available the script will fail to execute.
These two variable below need to be defined with the complete input file paths:
  _INPUT_FILE_DAY_1='day_1_snap.csv'
  _INPUT_FILE_DAY_2='day_2_snap.csv'
  
  if not path is given the script assumes the files resides in the same directory as itself.
  
the script can be executed as : 
python show_status.py -c




