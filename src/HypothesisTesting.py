import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#functions to prepare dataframes:
def new_df_from_col(df, list_columns):
    '''
    Returns new dataframe given old df and list of columns from old df
    '''
    new_df = df[list_columns]
    return new_df 


def merge_dfs(df1,df2):
    '''
    Takes in two dataframes and returns merged dataframe using left join on 'primaryid'
    '''
    return df1.merge(df2,on='primaryid',how='left')


drug_df = pd.read_csv('drug_fda.csv')
new_drug_df = new_df_from_col(drug_df, ['primaryid', 'caseid', 'drug_seq', 'role_cod', 'drugname',
       'val_vbm', 'cum_dose_chr', 'cum_dose_unit', 'lot_num'])

demo_df = pd.read_csv('demo_fda.csv')
new_demo_df = new_df_from_col(demo_df,['primaryid', 'caseid', 'caseversion', 'age', 'age_cod',
       'sex', 'wt', 'wt_cod', 'occp_cod', 'reporter_country', 'occr_country',
       'occp_cod_num'])

outcomes_df = pd.read_csv('outcomes_fda.csv')
reactions_df = pd.read_csv('reaction_fda.csv')


drug_demo = merge_dfs(new_drug_df, new_demo_df)
drug_demo_outcomes = merge_dfs(drug_demo, outcome_df)
merged_df = merge_dfs(drug_demo_outcomes, reactions_df)

#Functions to clean certain "messy" columns of interest to me and hypothesis testing
def code_to_numeric(code):
    '''
    Converts patient age to age in years
    '''
    if code == 'DY':
        return 1/365
    if code == 'YR':
        return 1
    if code == np.nan:
        return 0
    if code == 'MON':
        return 1/12
    if code == 'DEC':
        return 10
    if code == 'WK':
        return 7/365
    if code == 'HR':
        return 1/8760

def weight_conversion(code):
    '''
    converts patient weight to weight in lbs
    '''
    if code == 'KG':
        return 2.20462
    if code == np.nan:
        return 0
    if code == 'LBS':
        return 1

   
#Age and weight column clean-up:
merged_df['age_multiplier'] = merged_df['age_cod'].map(code_to_numeric)
merged_df['age_in_years'] = merged_df['age'] * merged_df['age_multiplier']
merged_df['age_group'] = (merged_df['age_in_years'] // 10) * 10 
merged_df['age'].round(0)
    
merged_df['weight_multiplier'] = merged_df['wt_cod'].map(weight_conversion)
merged_df['wt_in_lbs'] = merged_df['weight_multiplier'] * merged_df['wt']


#Filtering 'extreme' outliers
merged_df = merged_df[merged_df['wt_in_lbs'] <= 500]
merged_df = merged_df[merged_df['age'] > 0]


#Creating abbreviated dataframe from merged df with columns of interest for hypothesis testing
abrv_df = new_df_from_col(merged_df, ['age_in_years','sex','age_group','drugname','outc_cod','occp_cod'])
abrv_df['age_in_years'] = abrv_df['age_in_years'].round(0)

np.mean(abrv_df['age_in_years']) #Avg age 58.0
np.median(abrv_df['age_in_years']) #Median 62.0

'''
Hypothesis Test: 

H0: There is no relationship between proportion of deaths related to adverse drug events among men and women.
Ha: There is a relationship between proportion of deaths related to adverse drug events between men and women.

Alpha level = 0.05

OUTC_COD KEY:
 ----------------
 DE Death
 LT Life-Threatening
 HO Hospitalization - Initial or Prolonged
 DS Disability
 CA Congenital Anomaly
 RI Required Intervention to Prevent Permanent Impairment/Damage
 OT Other Serious (Important Medical Event)
'''

#Chi-squared test for independence:
def chisquare_test(outcome_code):
    '''
    Returns contingency_table for chi-squared test for independence 
    '''
    outcome_codes = pd.get_dummies(abrv_df['outc_cod'])
    mask = abrv_df['sex'] == 'M'
    mask2 = abrv_df['sex'] == 'F'

    male = outcome_codes[mask]
    female = outcome_codes[mask2]

    grouped_summed_male = male.groupby(abrv_df['age_group']).aggregate(sum)
    grouped_summed_female = female.groupby(abrv_df['age_group']).aggregate(sum)

    grouped_summed_male['Deaths_Male'] = grouped_summed_male[outcome_code]
    grouped_summed_female['Deaths_Female'] = grouped_summed_female[outcome_code]
    
    contingency_table = pd.concat([grouped_summed_male['Deaths_Male'], grouped_summed_female['Deaths_Female']], axis=1).dropna().reset_index()

    return contingency_table

#     chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
#     stats.chi2_contingency(contingency_table)


# Graphing for all outcome codes (other than death):
fig, axs = plt.subplots(3, 2, figsize=(18,30))
outcome_codes = ['LT','HO', 'DS', 'CA', 'RI', 'OT','DE']

for ax, code in zip(axs.flatten(), outcome_codes):
    contingency_table = chisquare_test(code)
    m_deaths = contingency_table['Deaths_Male']
    f_deaths = contingency_table['Deaths_Female']
    categories = contingency_table['age_group'].apply(str)
    ax.bar(categories, m_deaths, color='#2A89A7')
    ax.bar(categories, f_deaths, bottom=m_deaths ,color='#9D496E')
    ax.legend(('Male', 'Female'))
    ax.set_xlabel('Age group', fontsize = 15)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.set_title(f'Proportion of {code} \n Among Men and Women by Age Group', fontsize=18)
    ax.set_ylabel('Frequency', fontsize=15)
    plt.savefig('proportions_outcomes.png')