# Adverse Drug Events: Identifying trends in adverse drug events to help tailor medications for patients

<img src="http://res.freestockphotos.biz/pictures/1/1167-closeup-of-pills-and-medicine-pv.jpg" alt="alt text" width="1300" height="400">

###### Image by Benjamin Miller(2)

### Description: 

The purpose of this capstone project is to use patient attributes such as age, weight, and gender to help predict the likelihood a patient will experience a side effect from a given drug. 

### Data Used:

The U.S. Food and Drug Administration (FDA) Adverse Event Reporting System (FAERS). FAERS is a database that is a collection of reported medication adverse events, medication errors, and product quality complaints. The database supports the post-marketing surveillance of drugs ('phase IV' trial). (1) For this capstone, 2018 Quarter 4 FAERS data was used. 

### Data Overview:

* 7 tables with case ID as common element to each: 
  * **Demographics**
    * 394,066 rows, 34 columns
  * **Drug information**
    * 1,546,835 rows, 22 columns
  * **Drug reaction**
    * 1,250,978 rows, 4 columns
  * **Outcomes**
    * 299,135 rows, 3 columns
  * Source of report
    * 21,075 rows, 3 columns
  * Treatment dates
    * 620,308 rows, 9 columns
  * indications
    * 1,064,664 rows, 4 columns

Additional information on this dataset may be found [here](https://pharmahub.org/app/site/resources/2018/01/00739/FDA-FAERS-Data-Dictionary.pdf)

### Minimum Viable Product (MVP) Objectives:

* MVP: Determine most commonly reported adverse event for a medication within each age group to determine probability of experiencing commonly reported adverse event.
* MVP+: MVP and determine the probability of experiencing commonly reported adverse event for a medication given patient's age and sex
* MVP++: MVP+ and determine if other patient attributes such as weight plays a potential role in experiencing side effects given a medication.

### Raw Data:

Data was loaded into pandas dataframes with columns of interest selected. This was done to conserve memory and runtime due to the large nature of these tables. I knew which columns I wanted to select by using `.head()`, `.describe()`, `.info()`, and `.columns` in addition to using [this data dictionary](https://pharmahub.org/app/site/resources/2018/01/00739/FDA-FAERS-Data-Dictionary.pdf). Of the 7 tables listed above, pertinent columns came from 4 tables (Demographics, Drug information, Drug reaction, and Outcomes), all 4 of which were merged into a single pandas dataframe. Due to the this database collecting reports from users, there were inconsistencies in the data collected primarily in the form of inconsistent measurement units. Take for example the following that came from the demographics table:

| **age**  | **age_cod** |
| ------------- | ------------- |
| 1.0  | DY  |
| 58.0  | YR  |
|60.0 | YR |

In the example above, the age column displayed the numeric value of a patient's age and in the age_cod column you can see DY (Day) and YR (Year). In order to get these units all on the same page the following function was used:

```
def code_to_numeric(code):
    '''
    Converts age units to age in years
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
        
 merged_df['age_multiplier'] = merged_df['age_cod'].map(code_to_numeric)
 ```
 A similar issue was encounteres with weight and unit conversion:
 
 ```
 def weight_conversion(code):
    '''
    converts weight units to weight in lbs
    '''
    if code == 'KG':
        return 2.20462
    if code == np.nan:
        return 0
    if code == 'LBS':
        return 1
 ```

### References:

(1) https://www.fda.gov/drugs/surveillance/questions-and-answers-fdas-adverse-event-reporting-system-faers

(2) http://www.freestockphotos.biz/stockphoto/1167
