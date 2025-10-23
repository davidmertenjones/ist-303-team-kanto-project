# Steps to run and test the application
## Environment to run the application
*	python 3.13.5
*	pip 25.1

## Steps to run the application
1.	Clone the entire project source code from github by running command below in command prompt. Make sure `git` is installed on your local machine.
```
git clone https://github.com/davidmertenjones/ist-303-team-kanto-project.git
```
2.	In command prompt, access the the directory " ist-303-team-kanto-project".
```
cd ist-303-team-kanto-project
```
3.	Create a virtual environment `venv`. (Note: In command prompt, make sure you are accessing same root folder where you have cloned source code in step 1.)
```
python -m env venv
```
4.	Activate the virtual environment on Mac or Linux OS.
```
source venv/bin/activate
```
5.	Install the packages you need from requirements.txt. 
```
(venv)% pip install -r requirements.txt
```
6.	Run the Flask application on your machine
```
flask –app app.py run
```
7.	The Flask application is accessible from http://127.0.0.1:5000
   
8.	Database is available under the “hospital_search/instance” folder named “database.db”.  If database is not available or accidentally deleted, you can setup the database using the `init_db.py` script.
```
python init_db.py
```  

## Steps to test the application
1.	Install pytest, pytest-flask, and pytest-coverage if they are not already installed
2.	In command prompt, navigate to the directory “hospital_search”
```
cd hospital_search
```
3.	Use the command below to run the tests 
```
pytest
```


# A Hospital Facilities Catalog

## PART A

### <ins>Overview</ins>  
The Hospital Facilities Catalog is a web application that standardizes how hospital facilities describe and publish their available medical services (e.g., urgent care, maternity care, children pediatrics, veterans’ facilities, and psychiatric facilities), making it easy for patients, providers, and administrators to discover, compare, and manage care options. The first release will focus on the Los Angeles area.

### <ins>Team Name</ins>  
Team Kanto

### <ins>Team Members</ins>  
David Merten-Jones, Eva Mui, Aashish Sunar, Aishwarya Pandian, Jennifer Long

### <ins>Stakeholders</ins>  
* Patients who need to browse, compare, and manage care options can quickly find the right facility or service.
* IT and Application Support Teams who ensure infrastructure, security, integration, and smooth operations.
* Healthcare Providers (physicians, nurses, specialists, therapists) who deliver and coordinate care can quickly compare facilities and streamline referrals.
* Hospital/Clinic Administrators who manage service offerings, availability, and workflows.  
* Healthcare Executives/Leadership who oversee strategy can leverage catalog insights to guide strategic planning and resource allocation.

### <ins>User Stories (MVP)</ins>  

### Search Hospital Facilities by Name, City, or ZIP

1.  As a patient, I want to search hospital facilities by name, city, or ZIP code in Los Angeles so I can quickly find the medical facility I need.  
  * Priority: 1	  
  * Estimate: Requires the service database and search functionality so users can filter services by location field. Estimated 5.5 days total.  
    * Extend service database with location fields: 1 day  
    * Add database query logic to support filtering by location: 2 days  
    * UI development for location search and results display: 2 days

### Browse Hospital by Facility Type

2. As a patient, I want to browse hospitals by facility type (e.g., urgent care, maternity care, pediatric services, veteran care, and psychiatric services) so I can quickly find the healthcare services I need.
  * Priority: 1	  
  * Estimate: Requires database of services as well as system to retrieve records based on user input through UI. Time spent to set up database and integrate search feature will be shared among several user tasks. Estimated 7.5 days total.  
    * Design core service database schema: 2 days  
    * Develop backend search for query processing and filtering: 3 days  
    * Build UI components for search and results: 2 days

### View Detailed Provider Information

3. As a patient, I want to view detailed provider information including name, address, phone number, ratings, and available service types (e.g., urgent care, maternity, pediatrics, veteran care, psychiatric services) so I can make informed decisions about my care.  
  * Priority: 1	  
  * Estimate: Requires expansion of the service database with detailed provider information and creating a detail page to display the information to users. Estimated 3.5 days total.  
    * Extend database with additional provider information fields: 1 day  
    * UI for provider detail page layout: 2 days

### Create New Accounts

4. As an IT administrator or application support team member, I want the ability to create and manage user accounts and assign role-specific access to services, configurations, settings, and tools so that users have the appropriate permissions.
  * Priority: 2  
  * Estimate: Requires implementing user registration and login with role-based access, email verification, and secure password handling. Estimated 6.5 days total.  
    * Create a UI page for user account creation: 3 days  
    * Extend database with additional user fields: username, email, location of residence, etc: 3 days

### View Available Services

5. As a healthcare provider, I want to view the types of services available at my facility (e.g., urgent care, maternity, pediatrics, veteran care, psychiatric services) so I can recommend appropriate options to patients.
  * Priority: 2	  
  * Estimate: Creating an alternate view of the catalogue specifically for providers. Estimated 3.5 days total.  
    * Filter services by provider/facility: 1 day  
    * UI for services specific to that facility: 2 days  
    
### Update Provider Offerings

6. As a hospital or clinic administrator, I want to add, update, or remove the services offered by my facility so that the information remains accurate and up to date for users.
  * Priority: 2	  
  * Estimate: Functionality for administrators to manage catalogue entries through adding, editing, or removing services through an administrator panel. Estimated 5.5 days total.  
    * Extend database logic to support create/update/delete operations: 1 day  
    * Implement backend logic to edit database according to management actions: 2 days  
    * UI for administrator panel: 2 days

### Enable User Ratings and Reviews

7. As a patient, I want to view and submit ratings and feedback for services I’ve received so I can share my experience with other patients and provide input to the hospital for improvement.

  * Priority: 2	  
  * Estimate: Requires creation of reviews and ratings system linked to users, along with UI for displaying that feedback. Estimated 6.5 days total.  
    * Create reviews data model: 2 days  
    * UI for review submission form and review display: 2 days  
    * UI for administrator moderation controls: 2 days


### <ins>User Stories (Non-MVP)</ins>  

### Search Based on Current Location

* As a patient, I want to search for medical services by category (e.g., lab tests, imaging, consultations) based on my current location in San Bernardino County and view the fastest route on a map so that I can easily access nearby care options.
  
  * Priority: 3	  
  * Estimate: Requires using browser location data and mapping integration through API call to filter services by proximity and display the fastest route. Estimated 6.5 days total.  
    * Setup browser geolocation: 1 day  
    * Extend query logic to filter services by proximity: 2 days  
    * Integrate with Google Maps API or something similar: 3 days

### Allow Administrators to Verify Status

* As an administrator, I want to be able to verify the status of healthcare providers requesting access so that only legitimate providers can add or edit service details.
  
  * Priority: 3	  
  * Estimate: Requires extending user profiles with credential fields, creating a submission process for documents, and letting admins approve or reject them. Estimated 5.5 days total.  
    * Extend user database with credential fields: 1 day  
    * UI for providers to upload proof: 2 days  
    * UI for administrator view to approve or reject: 2 days

### Compare Costs

* As a patient, I want to check insurance coverage and out-of-pocket costs for each service so that I can make informed financial decisions.
  
  * Priority: 4	  
  * Estimate: Requires extending the service database with pricing and insurance details, and a system for cost calculation. Estimated 5.5 days total.  
    * Extend service database with cost and insurance fields: 1 day  
    * Backend calculation for coverage and copay/deductible: 2 days  
    * UI for cost breakdown: 2 days

### Statistical Reporting for Administrators

* As an administrator, I want to generate reports on service usage and demand so that I can make data-driven decisions.
  
  * Priority: 4	  
  * Estimate: Requires storing and aggregating service usage data, and then creating admin reporting tools with visualization and export options. Estimated days 6.5 days total.  
    * Set up data analytics model: 3 days  
    * UI for admin report of statistics: 2 days  
    * Option to export data: 1 day

### <ins>Project Time Estimate</ins>  
The Minimum Viable Product (MVP) will deliver all Priority 1 and Priority 2 user stories.
* Time Estimate — MVP: 38.5 days  
* Time Estimate — Non-MVP: 24 days  
* Total Estimated Effort: 62.5 days



## PART B
The user stories for Milestone 1.0 are broken into tasks, with team members assigned and set milestone targets for each iteration.

 
### <ins>Priority 1</ins>
#### Milestone 1 Iteration 1 
1.  As a patient, I want to search hospital facilities by name, city, or ZIP code in Los Angeles so I can quickly find the medical facility I need.  
    * Identify publicly source facility & services datasets (3 days) - Aishwarya
    * Define data schema, clean up data and create CSV (4 days) - David
      * Added function to convert .csv files to sqlite3 database - David
      * see [database_setup](https://github.com/davidmertenjones/ist-303-team-kanto-project/edit/main/README.md#:~:text=HospitalGenInfo-,database_setup,-2025%2D09%2D08)
    * UI/UX design and review (3 days) – Jennifer, Eva, Aishwarya
      * Search hospital facilities by name
      * Search hospital facilities by city
      * Search hospital facilities by ZIP
      * Return results
    * App development (7 days) – Aashish, David
      * Implement schema and ingest CSV
      * Create a Skelton Flask application with a landing page to:
         * Search hospital facilities
         * Return results
      * Add option to search hospital by name, city, or ZIP code
    * Define acceptance criteria (1 day) - Aishwarya
    * Test development (3 days) - Jen
      
2.  As a patient, I want to browse hospitals by facility type (e.g., urgent care, maternity care, pediatric services, veteran care, and psychiatric services) so I can quickly find the healthcare services I need.
    * UI/UX design and review (3 days) – Jennifer, Eva, Aishwarya
      * Add option to browse hospital by facility type on the landing page
      * Create a new page to allow users to browse hospitals by facility type
         * Urgent care
         * Maternity care
         * Pediatric services
         * Veteran care	
         * Psychiatric services 	
      * Return results		
    * App development (7 days) – Aashish, David
    * Define acceptance criteria (1 day) – Aishwarya
    * Test development (3 days) - Jen


#### Milestone 1 Iteration 2
3. As a patient, I want to view detailed provider information including name, address, phone number, ratings, and available service types (e.g., urgent care, maternity, pediatrics, veteran care, psychiatric services) so I can make informed decisions about my care.  
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * Return details provide information when user selects a hospital facility from the returned list which includes:	
         * Hospital facility name
         * Address
         * Phone number
         * Available service types
   * App development (7 days) – Aashish, David
   * Define acceptance criteria – Aishwarya
   * Test development (3 days) - Jen

      
### <ins>Velocity</ins> 
* Timeline: 4 weeks to milestone 1
* Iteration: Every two weeks
* User Stories: 3
* Starting Velocity: 22.7%
  * Scheduled Story Points: 22 story points as of Week 5
  * Completed Story Points: 5 story points as of Week 5
* Burndown Chart as of Week 5:\
  https://github.com/user-attachments/assets/8bb94f03-312c-4cc0-9382-d82f9fe2f27a 


### <ins>Milestone 2</ins>
The user stories for Milestone 2.0 are broken into tasks, with team members assigned and set milestone targets for each iteration.

4. As an IT administrator or application support team member, I want the ability to create and manage user accounts and assign role-specific access to services, configurations, settings, and tools so that users have the appropriate permissions.
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
    * Login option
    * App development (7 days) – Aashish, David
      * Create Account (patient, provider, or administrator)
      * Enable role-based access
    * Test development (2 days) - Jen

5. As a healthcare provider, I want to view the types of services available at my facility (e.g., urgent care, maternity, pediatrics, veteran care, psychiatric services) so I can recommend appropriate options to patients.
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * View ratings and feedback
      * Provide ratings and feedback	
    * App development (3 days) – Aashish, David
    * Test development (2 days) - Jen

6. As a hospital or clinic administrator, I want to add, update, or remove the services offered by my facility so that the information remains accurate and up to date for users.
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * View catalog of services
    * App development (2 days) – Aashish, David
    * Test development (2 days) - Jen

7. As a patient, I want to view and submit ratings and feedback for services I’ve received so I can share my experience with other patients and provide input to the hospital for improvement.
    * UI/UX design and review (3 days) – Jennifer, Eva, Aishwarya
      * Add services
      * Remove services
      * Edit services	
    * App development (3 days) – Aashish, David
    * Test development (2 days) - Jen
    * Demo preparation (7 days) - Team
  
## PART C
Refer to [“Steps to run and test the application”](#steps-to-run-and-test-the-application) section of this README to run and test the application.

### Project Dashboard
https://github.com/users/davidmertenjones/projects/1

### Test Strategies
**User Story 1 : Search Hospital Facilities by Name, City, or ZIP**
As a patient, I want to search hospital facilities by name, city, or ZIP code in Los Angeles so I can quickly find the medical facility I need.

**Acceptance Criteria:** 
* A search option allows users to search hospitals by name, city, or ZIP code in Los Angeles
* The results page should display the name, address, phone number, and available services for the selected hospital facility

**Possible Testing options:**  
* Partial matches 
* No results
* Case sensitivity
* Fuzzy search 
* Information that is pulled from the database accurately reflects the user’s search input

**User Story 2 : Browse Hospital by Facility Type**
As a patient, I want to browse hospitals by facility type (e.g., urgent care, maternity care, pediatric services, veteran care, and psychiatric services) so I can quickly find the healthcare services I need.

**Acceptance Criteria:** 
* Provides an option to allows users to browse hospitals by medical speciality.
* The search result should display a list of hospital facilities based on the medical specialty selected by the user.
* The results page should display the name, address, phone number, and available services for the selected hospital facility

** User story 3 : View Detailed Provider Information
As a patient, I want to view detailed provider information including name, address, phone number, ratings, and available service types (e.g., urgent care, maternity, pediatrics, veteran care, psychiatric services) so I can make informed decisions about my care.  

**Acceptance Criteria:**
* Each hospital facility returned based on the user's selection should include details such as the facility name, address, phone number, and available services.
* If no results are found, a clear message such as “No matching services found” is displayed.

**Summary**
| User Stories | Description | Testing Strategy |
| :----- | :------ | :---------- |
| 1   | As a patient, I want to search hospital facilities by name, city, or ZIP code in Los Angeles so I can quickly find the medical facility I need. | <ul><li>Implement automated tests to validate user input handling and search logic.</li><li>Perform manual UI testing to ensure users can search hospital facilities by name, city, or ZIP code within Los Angeles.</li><li>Verify that search results accurately reflect data retrieved from the database and match the user’s input criteria.</li></ul> |
| 2   | As a patient, I want to browse hospitals by facility type (e.g., urgent care, maternity care, pediatric services, veteran care, and psychiatric services) so I can quickly find the healthcare services I need. | Perform manual UI testing to ensure: <ul><li>The application provides an option for users to browse hospitals by medical specialty.</li><li>The results page displays a list of hospital facilities that match the selected medical specialty.</li><li>Verify that search results accurately reflect data retrieved from the database and match the user’s input criteria.</li></ul> |
| 3   | As a patient, I want to view detailed provider information including name, address, phone number, ratings, and available service types (e.g., urgent care, maternity, pediatrics, veteran care, psychiatric services) so I can make informed decisions about my care. | <ul><li>Each hospital facility listed includes details such as name, address, phone number, available services.</li><li>If no results are found, a clear message such as “No matching services found” is displayed.</li></ul> |




