# Schedule by d0jyaaan

## Table of Contents
+ [About](#about)
+ [Usage](#usage)
+ [Overview](#overview)
+ [Algorithm](#algorithm)

## About <a name = "about"></a>
<p>
  This is an application that given the input of 2 CSV files, will generate a timetable schedule.
  
  <br>
  
  Programming languages:
  <ul>
    <li>Python</li>
    <li>Html</li>
    <li>CSS</li>
  </ul>
  
  Framework:
  <ul>
    <li>Flask</li>
  </ul>
  
## Usage <a name="usage"></a>
  
  Execute the following:
  ```
  python app.py
  ```
  *Note that **debug** mode is on*
  
  ### Video Example on How to Use The Application
  <br>
  
  [![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/eGptFkUA1AI/0.jpg)](https://www.youtube.com/watch?v=eGptFkUA1AI)
   
 <br>
 
  ### Example of Generated Timetable
  ![Screenshot (689)](https://user-images.githubusercontent.com/65117301/158777896-eebd9c9d-3939-40a6-9856-d9fd205f03d6.png)
  
## Overview <a name="overview"></a>
### Advantages
  ```
  - Simple to program
  - Dynamic
  - Has a low runtime
  ```
  
  ### Disadvantages
  ```
  - Sometimes wont generate an acceptable timetable
  - Timetable can't be arranged according to teacher's preference
  ```
  
## Algorithm <a name="algorithm"></a>

  ### Parameters of Generating a Timetable
  ```
  - Availability of the subject teacher
  - Number of periods a subject has
  - Subjects can only have 1 period each day
  ```
  
  ### Understanding
  The algorithm used to generate the timetable is a random generator algorithm. It will random select a slot and a subject then try to assign them.
  After assigning them, it will remove the selected subject from the domain of other slots in the same day. If the number of periods of a subject reaches its maximum,   the algorithm will remove the subject from all the domains of slots in the class.
   
  This application is dynamic as it will always generate a timetable no matter how many classes and subjects are given.
  
  
  ### Class Objects
  There are 3 class objects that are used in generating the timetable:
  <ul>
  <li>Class_details</li>
  <li>Subject</li>
  <li>Timetable</li>
  </ul>
  
  ### Brief Overview of Class Objects
  
  <hr>
  
  ### Class_details
  This a class object that is used to store details of a class
  The details are: 
  ```
  - subjects [ List of integers which are codes corresponding to their subject ]
  - teachers [ List of tuples formated as ( subject , teacher ) ]
  ```
  
  ### Subject
  This is a class object that stores details of a subject
  The details are: 
  ```
  - subject name
  - limit of how many periods this subject should have
  - teachers [ List of teacher name ]
  ```
  
  ### Timetable
  This is a class object which stores the structure of a timetable
  Functions within this class object:
  ```
  - generate [ Generate an empty timetable ]
  - get_available [ Returns all the available slots in the timetable ]
  ```
  
</p>
