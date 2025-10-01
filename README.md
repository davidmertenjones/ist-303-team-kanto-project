# A Hospital Facilities Catalog 

## PART A

### <ins>Overview</ins>  
The Hospital Facilities Catalog is a web application that standardizes how hospital facilities describe and publish their available medical services (e.g., imaging, labs, surgery centers, urgent care), making it easy for patients, providers, and administrators to discover, compare, and manage care options. The first release will focus on the Los Angeles area.

### <ins>Team Name</ins>  
Team Kanto

### <ins>Team Members</ins>  
David Merten-Jones, Eva Mui, Aashish Sunar, Aishwarya Pandian, Jennifer Long

### <ins>Stakeholders</ins>  
* Patients who need to browse, compare, and manage care options can quickly find the right facility or service.
* Healthcare Providers (physicians, nurses, specialists, therapists) who deliver and coordinate care can quickly compare facilities and streamline referrals.
* Hospital/Clinic Administrators who manage service offerings, availability, and workflows.  
* IT and Application Support Teams who ensure infrastructure, security, integration, and smooth operations.  
* Healthcare Executives/Leadership who oversee strategy can leverage catalog insights to guide strategic planning and resource allocation.

### <ins>User Stories (MVP)</ins>  


### Browse Available Services by Hospital Facilities

* As a patient, I want to browse available services and find out which hospitals provide them (e.g., lab tests, imaging, surgery centers, urgent care) so I can quickly find what I need.  
  * Priority: 1	  
  * Estimate: Requires database of services as well as system to retrieve records based on user input through UI. Time spent to set up database and integrate search feature will be shared among several user tasks. Estimated 7.5 days total.  
    * Design core service database schema: 2 days  
    * Develop backend search for query processing and filtering: 3 days  
    * Build UI components for search and results: 2 days

### Search Hospital Facilities by Name, City, or ZIP

* As a patient, I want to search hospital facilities by name, city, or ZIP code in Los Angeles so I can quickly find the medical facility I need.  
  * Priority: 1	  
  * Estimate: Requires expansion of the service database and search functionality so users can filter services by location field. Estimated 5.5 days total.  
    * Extend service database with location fields: 1 day  
    * Add database query logic to support filtering by location: 2 days  
    * UI development for location search and results display: 2 days

### View Detailed Provider Information

* As a patient, I want to view detailed provider information including name, phone, fax, address, website, hours of operation, and available services so that I have all the necessary details to make informed care decisions.
  
  * Priority: 1	  
  * Estimate: Requires expansion of the service database with detailed provider information and creating a detail page to display the information to users. Estimated 3.5 days total.  
    * Extend database with additional provider information fields: 1 day  
    * UI for provider detail page layout: 2 days

### Create Account

* As a user (patient, provider, or administrator), I want the option to create an account so that I can access features and role-specific tools.  
  
  * Priority: 2  
  * Estimate: Requires implementing user registration and login with role-based access, email verification, and secure password handling. Estimated 6.5 days total.  
    * Create a UI page for user account creation: 3 days  
    * Extend database with additional user fields: username, email, location of residence, etc: 3 days

### Ratings/Reviews

* As a patient, I want to view and provide ratings or feedback on completed services so that I can share my experience with others and the hospital.  

  * Priority: 2	  
  * Estimate: Requires creation of reviews and ratings system linked to users, along with UI for displaying that feedback. Estimated 6.5 days total.  
    * Create reviews data model: 2 days  
    * UI for review submission form and review display: 2 days  
    * UI for administrator moderation controls: 2 days

### Provider Offerings

* As a provider, I want to view the catalog of services offered in my facility so that I can recommend appropriate options to patients.  

  * Priority: 2	  
  * Estimate: Creating an alternate view of the catalogue specifically for providers. Estimated 3.5 days total.  
    * Filter services by provider/facility: 1 day  
    * UI for services specific to that facility: 2 days  
    
### Update Provider Offerings

* As an administrator, I want to add, edit, or remove services in the catalog so that offerings remain accurate and up to date.  

  * Priority: 2	  
  * Estimate: Functionality for administrators to manage catalogue entries through adding, editing, or removing services through an administrator panel. Estimated 5.5 days total.  
    * Extend database logic to support create/update/delete operations: 1 day  
    * Implement backend logic to edit database according to management actions: 2 days  
    * UI for administrator panel: 2 days

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
#### Iteration 1 
1.  As a patient, I want to browse available services and find out which hospitals provide them (e.g., lab tests, imaging, surgery centers, urgent care) so I can quickly find what I need.
    * Define scope and objectives (0.5 days)
    * Identify stakeholders (patients, providers, administrators, IT teams, executives) (0.5 day)
    * Assign team roles and responsibilities (0.5 day)
    * Create initial timeline and milestones (0.5 day) 
    * Identify/publicly source facility & services datasets (3 days) - Aishwarya
    * Define data schema, clean up data and create CSV (4 days) - David
    * UI/UX design and review (3 days) – Jennifer, Eva, Aishwarya
      * Decide care pathing: urgent vs. non-urgent flows.
        * Urgent care: return hospitals/urgent care centers that provide urgent services
        * Non-urgent care: browse services (e.g., labs, imaging, surgery) and show which hospitals provide them
    * App development (7 days) – Aashish, David
      * Implement schema and ingest CSV.
      * Build search & results UI for urgent and non-urgent flows.
    * Test development (3 days) - ?
    * Document README with setup (1 day) - Aashish, David
    * Validate README with setup (1 day) - Jennifer, Eva, Aishwarya
    * Create burndown chart (1day) - Eva

2. As a patient, I want to search hospital facilities by name, city, or ZIP code in Los Angeles so I can quickly find the medical facility I need.  
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * Search hospital facilities by name
      * Search hospital facilities by city
      * Search hospital facilities by ZIP
    * App development (3 days) – Aashish, David
    * Build search & results UI
    * Test development (2 days) - ?

#### Iteration 2
3. As a patient, when I select a facility, I want to view detailed information including name, phone, fax, address, website, hours of operation, and available services so that I have all the necessary details to make informed care decisions.
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * Return hospital facilities information including name, phone, fax, address, website, hours of operation, and available services 
    * App development (3 days) – Aashish, David
    * Test development (2 days) - ?
      
### <ins>Velocity</ins> 
* Timeline: 4 weeks to milestone 1
* Iteration: Every two weeks
* User Stories: 3
* Starting Velocity: 22.7%
  * Scheduled Story Points: 22 story points as of Week 5
  * Completed Story Points: 5 story points as of Week 5
* Burndown Chart as of Week 5:\
  https://github.com/user-attachments/assets/8bb94f03-312c-4cc0-9382-d82f9fe2f27a 


### <ins>Priority 2</ins>
The user stories for Milestone 2.0 are broken into tasks, with team members assigned and set milestone targets for each iteration.

4. As a user (patient, provider, or administrator), I want the option to create an account so that I can access features and role-specific tools.  
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
    * Login option
    * App development (7 days) – Aashish, David
      * Create Account (patient, provider, or administrator)
      * Enable role-based access
    * Test development (2 days) - ?

5. As a patient, I want to view and provide ratings or feedback on completed services so that I can share my experience with others and the hospital.  
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * View ratings and feedback
      * Provide ratings and feedback	
    * App development (3 days) – Aashish, David
    * Test development (2 days) - ?

6. As a provider, I want to view the catalog of services offered in my facility so that I can recommend appropriate options to patients.  
    * UI/UX design and review (2 days) – Jennifer, Eva, Aishwarya
      * View catalog of services
    * App development (2 days) – Aashish, David
    * Test development (2 days) - ?

7. As an administrator, I want to add, edit, or remove services in the catalog so that offerings remain accurate and up to date.  
    * UI/UX design and review (3 days) – Jennifer, Eva, Aishwarya
      * Add services
      * Remove services
      * Edit services	
    * App development (3 days) – Aashish, David
    * Test development (2 days) - ?
    * Demo preparation (7 days) - Team
