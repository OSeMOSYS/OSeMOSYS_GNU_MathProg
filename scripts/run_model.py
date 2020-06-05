def run_model(data_file, model_file, destination):
# this function calculates the solutions of a data_file give which type of OSeMOSYS version the user chooses.
# data_file : should be the name of one of the existing data files in inputs (without extension)
# model_file : long, short, fast

    import pandas as pd
    import os
    import subprocess 

    ### Check Inputs
    if model_file !='long' and model_file !='short' and model_file != 'fast':
        return print('you selected the wrong model, choose between "long", "short" and "fast"')
    try:
        with open ('inputs/'+data_file+'.txt') as file:
            data_text = file.read()   
    except: print('you selected the wrong data file, choose one of the existing data files in "inputs" (without extension)')     

    data_file_loc = 'inputs/'+data_file+'.txt'

    ### Set in data_file the location where to save the solution
    
    # set Result Path parameter
    if 'param ResultsPath := ' in data_text:                # check if ResultsPath is assigned
        dr = data_text.split('param ResultsPath := ')       # split the string after ResultsPath := ( in this way the first part of the new string would contain the destination of the solution folder)
        i=dr[1].find(';')                                   # find location of first ; in new string 
        l = dr[1][0:i]                                      # read value of ResultsPath
        data_text=data_text.replace(l,'"'+destination+'"')  # replace it with new destination
    else:
        data_text = '\nparam ResultsPath := "'+destination+'";\n'+ data_text    # if ResultPath is not assigned then add a line at the beginning of the data_file and assign it
    
    with open('inputs/'+data_file+'.txt', 'w') as file:  # save modified data_file
        file.writelines(data_text)    
        
    ### Set model    
    if model_file == 'long':
        model_file_loc = 'src/osemosys.txt'
    elif model_file == 'short':
        model_file_loc = 'src/osemosys_short.txt' 
    elif model_file == 'fast':
        model_file_loc = 'src/osemosys_fast.txt'      

    ### Create Folder to save results
    if not os.path.exists(destination):
         os.makedirs(destination)
    
    ### Run model
    arguments = ["glpsol", "-m", model_file_loc, "-d", data_file_loc]
    output = subprocess.run(arguments, capture_output=True)#, text=True)
    output, os.path.join(destination)         
    ### need to find a way to stop when model resolution fails
    # as of now it just skips and keeps the previous results