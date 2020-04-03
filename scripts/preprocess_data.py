"""Pre-process OSeMOSYS data file to reduce matrix generation time

This script pre-processes an OSeMOSYS input data file by adding lines that list 
commodity-technology-mode combinations that data is provided for. Pre-processing 
a data file before starting a model run significantly reduces the time taken 
for matrix generation. 

 Pre-processing consists of the following steps:

1. Reading the ``InputActivityRatio`` and ``OutputActivityRatio`` sections of the 
data file to identify commodity-technology-mode combinations that data has been 
explicitly provided for.
2. Adding a set entry for each commodity that lists all technology-mode combinations 
that are associated with it.  
3. Values from the ``InputActivityRatios`` and ``OutputActivityRatios`` sections are 
added to the sets ``MODExTECHNOLOGYperFUELin`` and ``MODExTECHNOLOGYperFUELout`` respectively.
4. Values from the ``TechnologyToStorage`` and ``TechnologyFromStorage`` sections 
are added to the sets ``MODExTECHNOLOGYperSTORAGEto`` and ``MODExTECHNOLOGYperSTORAGEfrom`` respectively.
5. All values for technology-mode combinations are added to the sets 
``MODEperTECHNOLOGY``.

 In order to start a model run with a pre-processed data file, the following sets 
need to be introduced to its associated OSeMOSYS model file::

    set MODEperTECHNOLOGY{TECHNOLOGY} within MODE_OF_OPERATION;
    set MODExTECHNOLOGYperFUELout{COMMODITY} within MODE_OF_OPERATION cross TECHNOLOGY;
    set MODExTECHNOLOGYperFUELin{COMMODITY} within MODE_OF_OPERATION cross TECHNOLOGY;
    set MODExTECHNOLOGYperSTORAGEto{STORAGE} within MODE_OF_OPERATION cross TECHNOLOGY;
    set MODExTECHNOLOGYperSTORAGEfrom{STORAGE} within MODE_OF_OPERATION cross TECHNOLOGY;

"""

import pandas as pd
import os, sys
from collections import defaultdict

def main(data_infile, data_outfile):

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
    storage_to = []
    storage_from = []
    emission_table = []

    with open(data_infile, 'r') as f:
        for line in f:
            if line.startswith('set YEAR'):
                start_year = line.split(' ')[3]
            if line.startswith('set COMMODITY'):  # Extracts list of COMMODITIES from data file. Some models use FUEL instead. 
                fuel_list = line.split(' ')[3:-1]
            if line.startswith('set FUEL'):  # Extracts list of FUELS from data file. Some models use COMMODITIES instead. 
                fuel_list = line.split(' ')[3:-1]
            if line.startswith('set TECHNOLOGY'):
                tech_list = line.split(' ')[3:-1]
            if line.startswith('set STORAGE'):
                storage_list = line.split(' ')[3:-1]
            if line.startswith('set MODE_OF_OPERATION'):
                mode_list = line.split(' ')[3:-1]
            if line.startswith('set EMISSION'):
                emission_list = line.split(' ')[3:-1]
            
            if line.startswith(";"):
                    parsing = False

            if parsing:
                if line.startswith('['):
                    fuel = line.split(',')[2]
                    tech = line.split(',')[1]
                    emission = line.split(',')[2]
                elif line.startswith(start_year):
                    years = line.rstrip(':= ;\n').split(' ')[0:]
                    years = [i.strip(':=') for i in years]
                else:
                    values = line.rstrip().split(' ')[1:]
                    mode = line.split(' ')[0]
                    
                    if param_current == 'OutputActivityRatio':    
                        data_out.append(tuple([fuel,tech,mode]))
                        for i in range(0,len(years)):
                            output_table.append(tuple([tech,fuel,mode,years[i],values[i]]))
                    
                    if param_current == 'InputActivityRatio':
                        data_inp.append(tuple([fuel,tech,mode]))   
                    
                    data_all.append(tuple([tech,mode]))

                    if param_current == 'TechnologyToStorage' or param_current == 'TechnologyFromStorage':
                        if not line.startswith(mode_list[0]):
                            storage = line.split(' ')[0]
                            values = line.rstrip().split(' ')[1:]
                            for i in range(0, len(mode_list)):
                                if values[i] != '0':
                                    storage_to.append(tuple([storage,tech,mode_list[i]]))
                    
                    if param_current == 'EmissionActivityRatio':
                        emission_table.append(tuple([emission, tech, mode]))
                  
            if line.startswith(('param OutputActivityRatio','param InputActivityRatio','param TechnologyToStorage','param TechnologyFromStorage', 'param EmissionActivityRatio')):
                param_current = line.split(' ')[1]
                parsing = True

    dict_out = defaultdict(list)
    dict_inp = defaultdict(list)
    dict_all = defaultdict(list)
    dict_stt = defaultdict(list)
    dict_stf = defaultdict(list)
    dict_emi = defaultdict(list)

    for fuel, tech, mode in data_out:
        dict_out[fuel].append((mode, tech))

    for fuel, tech, mode in data_inp:
        dict_inp[fuel].append((mode, tech))
        
    for tech, mode in data_all:
        if mode not in dict_all[tech]:
            dict_all[tech].append(mode)
            
    for storage, tech, mode in storage_to:
        dict_stt[storage].append((mode, tech))

    for storage, tech, mode in storage_from:
        dict_stf[storage].append((mode, tech))

    for emission, tech, mode in emission_table:
        dict_emi[emission].append((mode, tech))
    
    print(dict_emi)
    
    def file_output_function(if_dict, str_dict, set_list, set_name, extra_char):
        for each in set_list:
            if each in if_dict.keys():
                line = set_name + str(each) + ']:=' + str(str_dict[each]) + extra_char
                if set_list == tech_list:
                    line = line.replace(',','').replace(':=[',':= ').replace(']*','').replace("'","")
                else:
                    line = line.replace('),',')').replace('[(',' (').replace(')]',')').replace("'","")
            else:
                line = set_name + str(each) + ']:='
            file_out.write(line + ';' + '\n')

    # Append lines at the end of the data file
    with open(data_outfile, 'w') as file_out: # 'a' to open in 'append' mode
        
        file_out.writelines(lines)
        
        file_output_function(dict_out, dict_out, fuel_list, 'set MODExTECHNOLOGYperFUELout[', '')
        file_output_function(dict_inp, dict_inp, fuel_list, 'set MODExTECHNOLOGYperFUELin[', '')
        file_output_function(dict_all, dict_all, tech_list, 'set MODEperTECHNOLOGY[', '*')
        
        if len(storage_list) > 1:
            file_output_function(dict_stt, dict_out, storage_list, 'set MODExTECHNOLOGYperSTORAGEto[', '')
            file_output_function(dict_stf, dict_out, storage_list, 'set MODExTECHNOLOGYperSTORAGEfrom[', '*')

        if len(emission_list) > 1:
            file_output_function(dict_emi, dict_emi, emission_list, 'set MODExTECHNOLOGYperEMISSION[', '')

        file_out.write('end;')

if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = "Usage: python {} <infile> <outfile>"
        print(msg.format(sys.argv[0]))
        sys.exit(1)
    else:
        data_infile = sys.argv[1]
        data_outfile = sys.argv[2]
        main(data_infile, data_outfile)