from run_model import run_model
from difference import difference
import os
import pandas as pd

### INPUTS
data_file = 'Tests_LS/test3'                 # name of data file in "inputs" (without extension)
models = ['long', 'short', 'fast']      # versions of OSeMOSYS to compare
folder = 'solutions/'+data_file               # location of solutions

### calculate solution with the various OSeMOSYS versions
for model_file in models:
    destination = folder+'/'+model_file
    run_model(data_file, model_file, destination)
    print('solved '+model_file)

### Check wehther there are differences in the solutions
d = 0
for file in os.listdir(folder+"/long"):
    filename = os.fsdecode(file)
    if filename != 'SelectedResults.csv': # Skip SelectedResults which is not a CSV
        df_long  = pd.read_csv(folder+'/long/'+filename)
        df_short = pd.read_csv(folder+'/short/'+filename)
        df_fast  = pd.read_csv(folder+'/fast/'+filename)

        if not df_long.equals(df_short):                                            # check if there is any difference
            d = d+1
            print("difference between long and short regarding file: "+filename)
            difference(df_long,df_short)                                            # function that shows the difference between the CSV files (absolute and relative errors)
            y = input('continue [y/n]: ')
            if y == 'n':
                break
        if not df_long.equals(df_fast):
            d = d+1
            print("difference between long and fast regarding file: "+filename)   
            difference(df_long,df_fast)
            y = input('continue [y/n]: ')
            if y == 'n':
                break
        if not df_short.equals(df_fast):
            d = d+1
            print("difference between short and fast regarding file: "+filename)
            difference(df_short,df_fast)
            y = input('continue [y/n]: ')
            if y == 'n':
                break

print('We found difference between '+str(d)+' files')

# import pandas as pd
# df_long  = pd.read_csv('solutions/test/long/AnnualVariableOperatingCost.csv')
# df_short  = pd.read_csv('solutions/test/short/AnnualVariableOperatingCost.csv')

# glpsol -m src/osemosys.txt -d inputs/data.txt 