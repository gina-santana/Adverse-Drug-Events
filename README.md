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
###### Table 1

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
 A similar issue was encountered with weight and unit conversion:
 
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
 
 
### Exploratory Data Analysis (EDA):
During exploration of this dataset, I explored patient attributes of potential interest such as sex, weight, and age. The distributions of age and weight are as follows:

###### Figure 1

![text](images/Age_distribution.png)

###### Figure 2

![text](images/pt_wt_distribution.png)


The distribution of patient age in years appears to be left-skewed and the distribution of patient weight in lbs appears to be right-skewed. The average age of the patients in this dataset was 58 years with median at 62 years. The average weight of patients in this dataset came out to 166 lbs and median of 158 lbs. I also explored the relationship of weight and age of the patients in this dataset as compared among men and women:

###### Figure 3

![text](images/Age_weight_scat.png)


The results of this comparison shows that the weight tends to drop off slightly after the average age and that in general it appears that men have higher weights than women. Nothing unexpected or surprising from these findings. To dig into the dataset, I wanted to explore 2 columns, 'outc_cod' (outcome codes) and 'occp_cod' (occupation code). The outcomes code column had the following possible values:

   * CA = congenital anomaly

   * DE = death

   * DS = disability

   * HO = Hospitalization - initial or prolonged

   * LT = life-threatening

   * OT = other serious (important medical event)

   * RI = required intervention to prevent permanent impairment/damage

The occupation code column (or what you can think of as the role of the reporter) had the following possible values:

   * MD = Physician

   * PH = Pharmacist

   * OT = Other health-professional

   * LW = Lawyer

   * CN = Consumer

Due to this dataset coming from a database of reports relating to adverse events to medications, I was interested in identifying the frequency of each of these outcomes occurring in addition to looking at who was primarily reporting these adverse events:

###### Figure 4

![text](images/reports_of_outcomes.png)

###### Figure 5

![text](images/report_sources_freq.png)

I was able to conclude from this exploratory analysis that the highest volume of adverse reactions had an outcome classified as other serious (important medical event) and that the highest volume of reports were coming directly from consumers. I decided to do hypothesis testing based on my findings related to outcomes, specifically the outcome of death. 

### Hypothesis Testing:
* Hypothesis Test # 1:

   H0: There is no relationship between proportion of deaths related to adverse drug events among men and women.
   
   Ha: There is a relationship between proportion of deaths related to adverse drug events between men and women.
   
   Statistical Test Used: Chi-Squared Test for Independence; alpha=0.05
   
   Results:
###### Table 2 

| **Result** | **Value** |
| -------- | ------- |
| chi2 | 9128.3 |
| p-value | 0.0000* |
| dof | 10 |


  *The p-value was rounded to 0.00 by ```stats.chi2_contingency()``` indicating that this p-value was very small to begin with.

  ###### Figure 6
  
  ![text](images/proportion_deaths.png)
  
  Although death was the primary outcome that was of interest to me, I looked further into the relative proportions of outcome occurences among men and women. 
  
  ###### Figure 7
  
  ![text](images/proportions_outcomes.png)
  
  What immediately stands out are the disproportionalities among several age groups in the outcome category for 'RI' or 'Required intervention to prevent             permanant impairment/damage' category. As a pharmacist, the questions that naturally came to mind was 'what are the drugs responsible?', 'Are these drugs           primarily used by women such as birth control?' and 'What was the top reported adverse event that caused the required intervention?'. My inquiries lead to the     following top 5 drugs reported with the outcome of 'RI':
###### Table 3  

| **Drug Name**  | **Report Frequency** | **Top Reported Adverse Event (proportional percentage)**  |
| ------------- | ------------- | -------------|
| Mirena  | 116  | Complication associated with device (4.3%)|
| Paraguard T 380A  | 61 | Headace; Pregnancy with contraceptive device (4.9%) |
| Nexplanon | 61 | Anxiety (4.9%) |
| Lisinopril  | 61  | Angioedema (31.1%) |
| Warfarin  |  57  | Anemia (8.8%) |

In the case of Mirena, an intrauterine device (IUD) used for birth control, the top reported adverse event that warrented intervention was due to complication associated with the device. Paraguard, another IUD used for birth control had headache and pregnancy with contraceptive device tied as the two top reported adverse events that warrented intervention. Nexplanon, an implant birth control device, had anxiety listed as it's most top reported averse event. It should be noted that anxiety for this outcome category was only reported 3 times with suicidal ideation reported 2 times. Lisinopril, a medication typically indicated for hypertension (high blood pressure) had the top reported adverse event of angioedema (swelling) is a well-studied side effect of this medication and it's drug class. This side effect warrants discontinuation of the medication. Lastly, warfarin, an anticoagulant (blood thinner) had anemia reported frequently associated with it with increased International Normalized Ratio (INR) closely following as the second common report. An increased INR puts a patient at increased risk of bleeding, making INR a tightly monitored and controlled medication due to its potential dangers if mismanaged. If an INR is increased enough, it would warrant immediate medical attention. 

In addition to 'RI' standing out (Figure 7), the category of 'CA' or 'congenital anomaly' had obvious disproportionalities in addition to an interesting distribution among ages. From a healtcare professional's standpoint, I wanted to know 'what are the drugs responsible?', 'what was the top reported adverse event that caused the congenital anomaly?'

###### Table 4

| **Drug Name**  | **Report Frequency** | **Top Reported Adverse Event (proportional percentage)**  |
| ------------- | ------------- | -------------|
| Zofran  | 1584  | Fetal exposure during pregnancy (3%) |
| Prednisolone  | 663 | Fetal exposure during pregnancy (7%) |
| Depakine Chrono | 577 | Fetal exposure during pregnancy (4.9%) |
| Norvir | 557  |  Fetal exposure during pregnancy (9.2%) |
| Tacrolimus |  478  | Fetal exposure during pregnancy (6.9%) |

Zofran is a medication used for antiemetic (anti-nausea) indications typically in patients undergoing chemotherapy. This medication may be prescribed to a woman during pregnancy to control morning sickness. The CDC has taken the stance that it may be ok to take during pregnancy based on a study done that suggests use of the drug during early pregnancy is not likely to cause birth defects (4). However, when considering other adverse events reported among the top 5 for Zofran, 'injury' (2%), 'atrial septic defect' (1.8%), and 'premature baby' (1.5%) appear. Utilizing additonal data for this would make for interesting data analysis. The second most reported drug for the 'CA' outcome was prednisolone. Prednisolone is a steroid used to reduce inflammation in various inflammatory conditions such as colitis and athritis to name a few. Fetal exposure during pregnancy was the top reported adverse event for this drug followed by: 'premature baby' (2.9%), 'low birth weight baby' (2.7%), 'exposure during pregnancy' (2.6%), and 'white blood cell count decreased' (2.4%). Depakine Chrono, a drug typically used to treat seizures and bipolar disorder, was also reported to have 'fetal exposure during pregnancy' as it's commonly reported adverse event. This was followed by 'dysmorphism' (3.1%), 'speech disorder developmental' (2%), 'disturbance in attention' (1.9%), and 'enuresis' (1.7%). Norvir, an HIV antiviral, had reports of fetal exposure during pregnancy in addition to: 'premature baby' (3.6%), 'spine malformation' (2.3%), 'anal atresia' (1.8%), and 'fibrosis' (1.8%). Lastly, tacrolimus is a drug typically used to prevent organ rejection post-transplant. Other than 'fetal exposure during pregnancy', the commonly reported adverse events were: 'heart disease congenital' (5%), 'ventricular septal defect' (3.8%), 'truncus asteriosis persistent' (3.8%), and 'cardiac septal defect' (3.3%).
  
### Interesting Finds:
* The top reported drug in this database is Xolair (omalizumab)
 * This medication is indicated for moderate to severe asthma and chronic idiopathic urticaria (3)
 * The top 5 reported adverse events related to Xolair in my dataset with their counts are as follows:
###### Table 5 

| **Adverse Event**  | **Frequency** |
| ------------- | ------------- |
| Decreased Weight  | 2579  |
| Dysnea  | 2348  |
|asthma | 2333 |
| Nasopharyngitis  | 2312   |
| Cough    |  2160  |

* When the data was grouped by age groups and sex I was able to identify the top reported medication for each of these groups:

###### Figure 8
![text](images/Top_drugs.png)

Not surprisingly, Xolair (the top reported drug in the entire dataset) appeared frequently throughout the different age/sex groups. This data can lend providers an idea of which medications to monitor more carefully or more frequently in patients of certain age/sex.

### Practical Use Cases: On Clinical Significance and conclusions
* Men and women are not equal when it comes to the proportion of certain outcomes related to medications, likewise with certain age groups. Information like this     can lend itself to knowing which medications should either be avoided for particular patients or monitored more carefully/frequently. 
* With the information provided in Table 5, regulatory agencies such as the FDA or CDC may be able to gain insight into trends relating to any misuse or             misprescribing of medications, which may lead to regulatory changes in the form of guidances, package insert information, drug class scheduling, etc. For           example, in Table 3, given that Lisinopril, a commonly prescribed medication in the US is one of the top 5 reported drugs associated with an interventional         outcome, and given that 31% have reported angioedema, the FDA may want to urge prescribers to consider alternative options or study it futher to determine what     demographic attributes are more likely to have the given outcome so as to avoid in certain patient populations. 
  * An additional example seen in Table 4 with Norvir, an HIV antiretroviral, may warrant further clinical trials in pregnancy. For reasons of efficacy, a             pregnant, female patient may not realistically be able to discontinue HIV medications during pregnancy. Alternatives to treatment or more frequent monitoring       of a patient on this antiviral medication during pregnancy may be warrented.

### Further studies:
* Linear regressions to predict likelihood of outcomes given handful of patient attributes such as age, sex, weight, and medication they are taking. This will be a potential direction for capstone 2. 

* Looking at additional trends in reports from previous or ongoing years of FAERS data relating to the top 5 drugs explored above in 'RI' and 'CA' outcome categories may provide actionable insight to regulatory agencies such as the FDA and CDC. This actionable insight may aid in identifying medications in need of black box warnings or updates to package inserts.

### References:

(1) https://www.fda.gov/drugs/surveillance/questions-and-answers-fdas-adverse-event-reporting-system-faers

(2) http://www.freestockphotos.biz/stockphoto/1167

(3) https://www.accessdata.fda.gov/drugsatfda_docs/label/2016/103976s5225lbl.pdf

(4) https://www.cdc.gov/ncbddd/birthdefects/features/kf-ondansetron-and-birth-defects.html
