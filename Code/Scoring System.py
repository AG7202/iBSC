#%%
#importing relevant packets (Pandas and Numpy)
#pip install pandas,openpyxl and numpy
import pandas as pd
import numpy as np
# %%
#Read in the demographics data as excel file
Demographics = pd.read_excel('/workspaces/iBSC/Data/Anonymised NACShock Demographics v2.xlsx')
# %%
#Convert to a dataframe
df1 = pd.DataFrame(Demographics)
print(df1.head())
# %%
#Add age scoring system
conditions = [
    (df1.Age < 50),
    (df1.Age >= 50) & (df1.Age <= 59),
    (df1.Age >= 60)
]
scores = [0, 1, 2]
df1['Age Score'] = np.select(conditions, scores)
print(df1[['Age', 'Age Score']].head())
# %%
#Add cumulative bypass time scoring system
conditions = [
    (df1.CumulativeBypassTime < 60),
    (df1.CumulativeBypassTime >= 60) & (df1.CumulativeBypassTime < 180),
    (df1.CumulativeBypassTime >= 180)
]
scores = [0, 1, 2]
df1['Cumulative Bypass Time Score'] = np.select(conditions, scores)
print(df1[['CumulativeBypassTime', 'Cumulative Bypass Time Score']].head())
# %%
#Add Sex scoring system
conditions = [
    (df1.SEX == 'M')
]
scores = [1]
df1['Sex Score']= np.select(conditions, scores, default=0)
print(df1[['SEX', 'Sex Score']].head())
# %%
#Add Surgery Type scoring system
conditions = [
    (df1.Cabg == 'No') & (df1.Valve == 'No'),
    (df1.Cabg == 'Yes') & (df1.Valve == 'No'),
    (df1.Cabg == 'No') & (df1.Valve == 'Yes'),
    (df1.Cabg == 'Yes') & (df1.Valve == 'Yes')
]
scores = [0, 1, 0, 3]
df1['Surgery Type Score'] = np.select(conditions, scores)
print(df1[['Cabg', 'Valve', 'Surgery Type Score']].head())
# %%
#Add Dialysis score
conditions = [
    (df1.Dialysis != 0)
]
scores = [2]
df1['Dialysis Score'] = np.select(conditions, scores, default=0)
print(df1[['Dialysis', 'Dialysis Score']].head())
print(df1['Dialysis Score'].unique())
# %%
#Liver Disease Scoring System
#conditions = [
 #   (df1.LiverDisease = 1)
#]
#scores =[2]
#df1['Liver Disease Score'] = np.select(conditions, scores, default=0)
#print(df1[['LiverDisease', 'Liver Disease Score']].head())
#print(df1['Liver Disease Score'].unique())

#%%
#Heart Failure Score
conditions = [
    (df1.LeftVentricularFunction < 50)
]
scores = [1]
df1['Heart Failure Score'] = np.select(conditions, scores, default=0)
print(df1[['LeftVentricularFunction', 'Heart Failure Score']].head())
print(df1['Heart Failure Score'].unique())
# %%
#Previous Cardiac Surgery Score
conditions = [
    (df1.PreviousCardiacSurgery != '0')
]
scores = [1]
df1['Previous Cardiac Surgery Score'] = np.select(conditions, scores, default=0)
print(df1[['PreviousCardiacSurgery', 'Previous Cardiac Surgery Score']].head())
print(df1['Previous Cardiac Surgery Score'].unique())
# %%
#Urgent Surgery Score
conditions = [
    (df1.OperativeUrgency != 'Elective')
]
scores = [1]
df1['Urgent Surgery Score'] = np.select(conditions, scores, default=0)
print(df1[['OperativeUrgency', 'Urgent Surgery Score']].head())
print(df1['Urgent Surgery Score'].unique())
# %%
#Amiodorone Score
#conditions = [
 #   (df1.drugs != 'Amiodorone Key Number')
#]
#scores = [2]
#df1['Amiodorone Score'] = np.select(conditions, scores, default=0)
#print(df1[['drugs', 'Amiodorone Score']].head())
#print(df1['Amiodorone Score'].unique())
# %%
#Beta-blocker score
df1['BBFlag'] = df1['DrugsOnAdmission'].str.contains('5')
df1['BB Score'] = np.where(df1['BBFlag'] == True, -1, 0)
print(df1[['DrugsOnAdmission', 'BB Score']].head())
# %%
#Type of Surgery Score
conditions = [
   (df1.Cabg == 'No') & (df1.Valve == 'No'),
   (df1.Cabg == 'Yes') & (df1.Valve == 'No'),
   (df1.Cabg == 'No') & (df1.Valve == 'Yes'),
   (df1.Cabg == 'Yes') & (df1.Valve == 'Yes')
]
scores = [0, 1, 0, 3]
df1['Type of Surgery Score'] = np.select(conditions, scores)
print(df1[['Cabg', 'Valve', 'Type of Surgery Score']].head())
# %%
#Calculate final score
df1['Final Score'] = (df1['Age Score'] + df1['Cumulative Bypass Time Score'] + df1['Sex Score'] + df1['Dialysis Score'] +
                    df1['Surgery Type Score'] + df1['Heart Failure Score'] + df1['Previous Cardiac Surgery Score'] +
                    df1['Urgent Surgery Score'] + df1['BB Score']) #+ Liver disease score + Amiodarone score

print(df1['Final Score'].head())
#%%
#Categorise into low, medium and high risk
conditions = [
    (df1['Final Score'] < 3),
    (df1['Final Score'] >= 3) & (df1['Final Score'] <= 6),
    (df1['Final Score'] > 6)
]
scores = [1,2,3] #1 = Low, 2 = Moderate, 3 = High
df1['Risk'] = np.select(conditions, scores)
print(df1[['Final Score', 'Risk']].head())
print(df1['Risk'].unique())
# %%
#Create new excel file with scores added
df1.to_excel('Demographics with Risk Score.xlsx', index=False)