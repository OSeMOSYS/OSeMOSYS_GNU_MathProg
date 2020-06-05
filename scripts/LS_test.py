import pandas as pd
import os
import subprocess 

## IDEA
## build script that for a given model calaculates the results with the three versions and saves the results in a manageable way

### Set location where to save the solution
#data_file = 'super_simple_model'
#data_file_loc ='inputs/super_simple_model.txt'
#with open('inputs/'+data_file+'.txt') as file:  
#    data_text = file.read() 

# set Result Path parameter
#if 'param ResultsPath := ' in data_text:
#    dr = data_text.split('param ResultsPath := ')
#    i=dr[1].find(';')
#    l = dr[1][0:i]
#    data_text=data_text.replace(l,'"solutions/'+data_file+'"')
#else:
#    data_text = data_text + '\nparam ResultsPath := "solutions/'+data_file+'"'



with open('inputs/'+data_file+'.txt', 'w') as file:  
    file.writelines(data_text)

# create folder for saving solutions
if not os.path.exists('solutions/'+data_file):
         os.makedirs('solutions/'+data_file)

# select model file

model_file = 'src/osemosys.txt'
arguments = ["glpsol", "-m", model_file, "-d", data_file_loc]
output = subprocess.run(arguments, capture_output=True)#, text=True)
output, os.path.join('solutions/'+data_file)         


# 3 Run OSemosys

#       select ´datafile
#       change name path in input
#       create solution foler
#       run model



# 4 save results

# 5 quickly compare results


# df2.equals(df1)   #Check If Two Dataframes Are Exactly Same

# pd.concat([df1,df2]).drop_duplicates(keep=False) # Find Rows Which Are Not common Between Two dataframes


#prod = pd.read_csv('solutions/indonesia/ProductionByTechnologyAnnual.csv')
#prod_s = pd.read_csv('solutions/indonesia_short/ProductionByTechnologyAnnual.csv')
#prod_f = pd.read_csv('solutions/indonesia_fast/ProductionByTechnologyAnnual.csv')





# There is somethinr interesting here on how to call osemosys from python

#arguments = ["glpsol", "-m", model_file, "-d", data_text]
#output = run(arguments, capture_output=True, text=True)
#return output, os.path.join(results_folder)