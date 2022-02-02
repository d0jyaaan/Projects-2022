# Duty List Generator

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting-started)
+ [Prerequisites](#prerequisites)
+ [Installing](#installing)

## About <a name = "about"></a>
This branch contains all the code for a duty list generator called **duty.py**. In **duty.py**, it contains multiple functions, which are:
```
  main
  idlist
  dutymaker
  dutylistprint
  excelmaker
```

**IMPORTANT: Please read the following to understand how the function works**

This python program takes in command line arguements where one of the arguements must be a **Key**.
<br>
There must be 2 CSV files present in the same directory as duty.py and must be named **idlist.csv** and **dutyspot.csv**.
<br>
The following are the format for the CSV files:

**idlist.csv**
```
  ID  |  NAME |   GRADE  |  COMMITTEE   |
  ----|-------|----------|--------------|
  int |  str  |    int   |  TRUE/FALSE  |
```
**dutyspot.csv**
```
  DUTY  |  NO. PEOPLE  |  DUTY TIME (Default is 3) |
  ------|--------------|---------------------------|
  str   |      int     |       TRUE/FALSE          |
```
The function **dutymaker** must be changed according to the number of duty times and the people that should duty.


## Getting Started <a name = "getting-started"></a>

### Prerequisites <a name = "prerequisites"></a>
```
The following are the imports used:
  - csv
  - random
  - copy
  - sys
  - datetime
  - xlsxwriter
```
The documentation of xlsxwriter can be found <a href="https://xlsxwriter.readthedocs.io/">here</a>.

## Installing <a name = "installing"></a>
Download **duty.py** in a folder and prepare **idlist.csv** and **dutyspot.csv**.
