# Adverse Drug Events: Predicting adverse drug event occurrences to help tailor medication prescriptions

<img src="http://res.freestockphotos.biz/pictures/1/1167-closeup-of-pills-and-medicine-pv.jpg" alt="alt text" width="1300" height="400">

###### Image by Benjamin Miller(2)

### Description: 

The purpose of this capstone project is to use patient attributes such as age, gender, and/or medication dosages to help predict the likelihood a patient will experience a side effect from a given drug. 

### Data Used:

The U.S. Food and Drug Administration (FDA) Adverse Event Reporting System (FAERS). FAERS is a database that is a collection of reported medication adverse events, medication errors, and product quality complaints.The database supports the post-marketing surveillance of drugs ('phase IV' trial). (1)

### Data Overview:

* 7 tables with case ID as common element to each: 
  * Demographics
    * 394066 rows, 34 columns
  * Drug information
    * 1546835 rows, 22 columns
  * Drug reaction
    * 1250978 rows, 4 columns
  * Outcomes
    * 299135 rows, 3 columns
  * Source of report
    * 21075 rows, 3 columns
  * Treatment dates
    * 620308 rows, 9 columns
  * indications
    * 1064664 rows, 4 columns

Additional information on this dataset may be found [here](https://pharmahub.org/app/site/resources/2018/01/00739/FDA-FAERS-Data-Dictionary.pdf)

### Minimum Viable Product (MVP) Objectives:

* MVP: Determine most commonly reported adverse event for a medication and use patient age/age-group to determine probability of experiencing commonly reported adverse event.
* MVP+: MVP and determine the probability of experiencing commonly reported adverse event for a medication given patient's age and sex
* MVP++: MVP+ and determine if other patient attributes such as weight plays a potential role in experiencing side effects given a medication.

### References:

(1) https://www.fda.gov/drugs/surveillance/questions-and-answers-fdas-adverse-event-reporting-system-faers

(2) http://www.freestockphotos.biz/stockphoto/1167
