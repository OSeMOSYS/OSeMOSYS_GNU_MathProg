def difference(df1, df2):
    import pandas as pd

    #df_long  = pd.read_csv('solutions/test/long/AnnualVariableOperatingCost.csv')
    #df_fast  = pd.read_csv('solutions/test/fast/AnnualVariableOperatingCost.csv')

    col_m = list(df1.columns)

    diff = pd.merge(df1,df2, on=col_m[0:-1])

    diff['err_abs'] = abs(diff['VALUE_x']-diff['VALUE_y'])
    diff['err_rel'] = abs(diff['VALUE_x']-diff['VALUE_y'])/abs(diff['VALUE_x'])
    diff = diff[(diff['err_abs']!=0) & (abs(diff['err_rel'])>0)]
    try: print('Maximum percentage Difference: '+str(max(abs(diff['err_rel'])))+' Mean Difference: '+str(diff['err_rel'].mean()))
    except: print('Not possible to calculate Maximum and mean')
    print(diff)
