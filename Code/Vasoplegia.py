#%%
#Import pandas and numpy and openpyxl
import pandas as pd
import numpy as np  

#%%
#Read in CO data
Cardiac = pd.read_excel('/workspaces/iBSC/Data/NACSHOCK Cardiac Output measured v1.xlsx')
CO = pd.DataFrame(Cardiac)
print(CO.head())
# %%
#Create a TPTD (0) or PAC flag (1)
conditions = [
    (CO.CO > 0)
]
scores = [ 1]
CO['CO Flag'] = np.select(conditions, scores)
print(CO[['CO', 'CCO', 'CO Flag']].head())
print(CO['CO Flag'].unique())   
# %% 
# #read in VIS data
Vasopressor = pd.read_excel('/workspaces/iBSC/Data/Anonymised NACShock VIS v2.xlsx')
VIS = pd.DataFrame(Vasopressor)
print(VIS.head())
#%%
#read in haemodynamics data
Haemodynamics = pd.read_excel('/workspaces/iBSC/Data/Anonymised NACShock Haemodynamics 2018-2023.xlsx')
Hd = pd.DataFrame(Haemodynamics)
print(Hd.head())

# %%
#Create a flag for the presence of a vasopressor
conditions = [
    (VIS.VASO_24h == 1),
    (VIS.ADR_24h == 1),
    (VIS.NADR_24h == 1),
]
scores = [1, 1, 1]
VIS['Vasopressor Flag'] = np.select(conditions, scores, default=0)
print(VIS[['VASO_24h', 'ADR_24h', 'NADR_24h', 'Vasopressor Flag']].head())

#%%
#Create low SVR and high CI flag
conditions = [
    (CO['SVR'] < 800) & (CO['CI'] > 2.5),
    (CO['SVR'] < 800) & (CO['CCI'] > 2.5),
    (CO['SVR_CCO'] < 800) & (CO['CI'] > 2.5),
    (CO['SVR_CCO'] < 800) & (CO['CCI'] > 2.5),
]
scores = [1, 1, 1, 1]
CO['Low SVR High CI Flag'] = np.select(conditions, scores, default=0)
print(CO[['SVR', 'CI', 'SVR_CCO', 'CCI', 'Low SVR High CI Flag']].head())
print(CO['Low SVR High CI Flag'].unique())
#%%
#Vasoplegia Flag
#need to create index of same length
conditions = [
    (VIS['Vasopressor Flag'] ==1) & (Hd['avgMAP_24h'] <= 60) & (Hd['avgMAP_24h'] >= 50) & (CO['Low SVR High CI Flag'] == 1)
]
scores = [1]
CO['Vasoplegia Flag'] = np.select(conditions, scores, default=0)
print(CO[['Vasopressor Flag', 'avgMAP_24h', 'Low SVR High CI Flag', 'Vasoplegia Flag']].head())
print(CO['Vasoplegia Flag'].unique())
# %%
# Combine relevant columns into a single DataFrame
#df = CO.copy()
#df['Vasopressor Flag'] = VIS['Vasopressor Flag']
#df['avgMAP_24h'] = Hd['avgMAP_24h']

#conditions = [
#    (df['Vasopressor Flag'] == 1) & 
#    (df['avgMAP_24h'] <= 60) & 
#    (df['avgMAP_24h'] >= 50) & 
#    (df['Low SVR High CI Flag'] == 1)
#]
#scores = [1]

#df['Vasoplegia Flag'] = np.select(conditions, scores, default=0)
#print(df[['Vasopressor Flag', 'avgMAP_24h', 'Low SVR High CI Flag', 'Vasoplegia Flag']].head())

# %%
#print(df['Vasoplegia Flag'].unique())
# %%
