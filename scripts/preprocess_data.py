import pandas as pd
import os, sys
from collections import defaultdict


data_infile = sys.argv[1]
data_outfile = sys.argv[2]

lines = []
with open(data_infile, 'r') as f1:
    for line in f1:
        if not line.startswith(('set MODEper','set MODEx', 'end;')):
            lines.append(line)
            
with open(data_outfile, 'w') as f2:
    f2.writelines(lines)

parsing = False

data_all = []
data_out = []
data_inp = []

output_table = []

with open(data_infile, 'r') as f:
    for line in f:
        if line.startswith('set YEAR'):
            start_year = line.split(' ')[3]
        if line.startswith('set COMMODITY'): # Extracts list of COMMODITIES from data file. Some models use FUEL instead. 
            fuel_list = line.split(' ')[3:-1]
        if line.startswith('set FUEL'): # Extracts list of FUELS from data file. Some models use COMMODITIES instead. 
            fuel_list = line.split(' ')[3:-1]
        if line.startswith('set TECHNOLOGY'):
            tech_list = line.split(' ')[3:-1]
        if line.startswith('set STORAGE'):
            storage_list = line.split(' ')[3:-1]
        if line.startswith('set MODE_OF_OPERATION'):
            mode_list = line.split(' ')[3:-1]
        if line.startswith(";"):
                parsing = False   
        if parsing:
            if line.startswith('['):
                fuel = line.split(',')[2]
                tech = line.split(',')[1]
            elif line.startswith(start_year):
                years = line.rstrip().split(' ')[0:]
                years = [i.strip(':=') for i in years]
            elif not line.startswith(start_year):
                values = line.rstrip().split(' ')[1:]
                mode = line.split(' ')[0]
                if param_current=='OutputActivityRatio':    
                    data_out.append(tuple([fuel,tech,mode]))
                    for i in range(0,len(years)):
                        output_table.append(tuple([tech,fuel,mode,years[i],values[i]]))
                
                if param_current=='InputActivityRatio':
                    data_inp.append(tuple([fuel,tech,mode]))   
                data_all.append(tuple([tech,mode]))
                
        if line.startswith(('param OutputActivityRatio','param InputActivityRatio')):
            param_current = line.split(' ')[1]
            parsing = True
        
        

""" with open(data_infile, 'r') as f:
    for line in f:
        if line.startswith(";"):
            parsing = False   
        if parsing:
            if line.startswith('['):
                fuel = line.split(',')[2]
                tech = line.split(',')[1]
            elif line.startswith(start_year):
                years = line.rstrip().split(' ')[0:]
                years = [i.strip(':=') for i in years]
            elif not line.startswith(start_year):
                values = line.rstrip().split(' ')[1:]
                mode = line.split(' ')[0]
                data_out.append(tuple([fuel,tech,mode]))
                data_all.append(tuple([tech,mode]))
                for i in range(0,len(years)):
                    output_table.append(tuple([tech,fuel,mode,years[i],values[i]]))
        if line.startswith('param OutputActivityRatio',):
            parsing = True

with open(data_infile, 'r') as f:
    for line in f:
        if line.startswith(";"):
            parsing = False   
        if parsing:
            if line.startswith('['):
                fuel = line.split(',')[2]
                tech = line.split(',')[1]
            elif not line.startswith(start_year):
                mode = line.split(' ')[0]
                data_inp.append(tuple([fuel,tech,mode]))
                data_all.append(tuple([tech,mode]))
        if line.startswith('param InputActivityRatio'):
            parsing = True """

# For TechnologyToStorage and TechnologyFromStorage 
storage_to = []
storage_from = []

with open(data_infile) as f:
    for line in f:
        if line.startswith(";"):
            parsing = False   
        if parsing:
            if line.startswith('['):
                tech = line.split(',')[1]
            elif not line.startswith(mode_list[0]):
                storage = line.split(' ')[0]
                values = line.rstrip().split(' ')[1:]
                for i in range(0,len(mode_list)):
                    if values[i] != '0':
                        storage_to.append(tuple([storage,tech,mode_list[i]]))
                        #data_all.append(tuple([tech,mode_list[i]]))
        if line.startswith(('param TechnologyToStorage','param TechnologyFromStorage')):
            param_current = line
            print(param_current.split(' ')[1])
            parsing = True

""" with open(data_infile) as f:
    for line in f:
        if line.startswith(";"):
            parsing = False   
        if parsing:
            if line.startswith('['):
                tech = line.split(',')[1]
            elif not line.startswith(mode_list[0]):
                storage = line.split(' ')[0]
                values = line.rstrip().split(' ')[1:]
                for i in range(0,len(mode_list)):
                    if values[i] != '0':
                        storage_from.append(tuple([storage,tech,mode_list[i]]))
                        #data_all.append(tuple([tech,mode_list[i]]))
        if line.startswith('param TechnologyFromStorage'):
            parsing = True
"""

dict_out = defaultdict(list)
dict_inp = defaultdict(list)
dict_all = defaultdict(list)
dict_stt = defaultdict(list)
dict_stf = defaultdict(list)

for fuel,tech,mode in data_out:
    dict_out[fuel].append((mode,tech))

for fuel,tech,mode in data_inp:
    dict_inp[fuel].append((mode,tech))
    
for tech,mode in data_all:
    if mode not in dict_all[tech]:
        dict_all[tech].append(mode)
        
for storage,tech,mode in storage_to:
    dict_stt[storage].append((mode,tech))

for storage,tech,mode in storage_from:
    dict_stf[storage].append((mode,tech))
'''        
# Open data file and delete line with 'end;' statement
lines = []
with open(data_infile, 'r') as f1:
    for line in f1:
        if not line.startswith('end;'):
            lines.append(line)


with open(data_outfile, 'w') as f2:
    f2.writelines(lines)
'''

# Append lines at the end of the data file
with open(data_outfile, 'w') as file_out: # 'a' to open in 'append' mode
    
    file_out.writelines(lines)

    for each in fuel_list:
        if each in dict_out.keys():
            line = 'set MODExTECHNOLOGYperFUELout[' + str(each)+']:=' + str(dict_out[each])
            line = line.replace('),',')').replace('[(',' (').replace(')]',')').replace("'","")
        else:
            line = 'set MODExTECHNOLOGYperFUELout[' + str(each) + ']:='
        file_out.write(line + ';' + '\n')
    
    for each in fuel_list:
        if each in dict_inp.keys():
            line = 'set MODExTECHNOLOGYperFUELin[' + str(each) + ']:=' + str(dict_inp[each])
            line = line.replace('),',')').replace('[(',' (').replace(')]',')').replace("'","")
        else:
            line = 'set MODExTECHNOLOGYperFUELin[' + str(each) + ']:='
        file_out.write(line + ';' + '\n')
    
    for each in tech_list:
        if each in dict_all.keys():
            line = 'set MODEperTECHNOLOGY[' + str(each) + ']:=' + str(dict_all[each]) + '*'
            line = line.replace(',','').replace(':=[',':= ').replace(']*','').replace("'","")
        else:
            line = 'set MODEperTECHNOLOGY[' + str(each) + ']:='
        file_out.write(line + ';' + '\n')
        
    if len(storage_list) > 1:
        for each in storage_list:
            if each in dict_stt.keys():
                line = 'set MODExTECHNOLOGYperSTORAGEto[' + str(each)+']:=' + str(dict_out[each])
                line = line.replace('),',')').replace('[(',' (').replace(')]',')').replace("'","")
            else:
                line = 'set MODExTECHNOLOGYperSTORAGEto[' + str(each) + ']:='
            file_out.write(line + ';' + '\n')
        
    if len(storage_list) > 1:
        for each in storage_list:
            if each in dict_stf.keys():
                line = 'set MODExTECHNOLOGYperSTORAGEfrom[' + str(each)+']:=' + str(dict_out[each])
                line = line.replace('),',')').replace('[(',' (').replace(')]',')').replace("'","")
            else:
                line = 'set MODExTECHNOLOGYperSTORAGEfrom[' + str(each) + ']:='
            file_out.write(line + ';' + '\n')
        
    file_out.write('end;')