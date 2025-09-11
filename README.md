**A Medical Service Catalog**

**PART A**

**Overview**  
A medical service catalog app is a Web application that centralizes and streamlines access to healthcare organizations’ available medical services, allowing patients, providers, and administrators to easily browse, request, and manage care options.  The initial rollout of this application will focus on serving the San Bernardino County area.

**Team Name**  
Team Kanto

**Team Members**  
David Merten-Jones, Eva Mui, Aashish Sunar, Aishwarya Pandian, Jennifer Long

**Stakeholders**  
* Patients who browse, request, and schedule medical services.  
* Healthcare Providers (physicians, nurses, specialists, therapists) who order, deliver, and coordinate patient services.  
* Hospital/Clinic Administrators who manage service offerings, availability, and workflows.  
* IT and Application Support Teams who ensure infrastructure, security, integration, and smooth operations.  
* Healthcare Executives/Leadership who use service catalog insights for strategic planning and resource allocation.

**User Stories (MVP)**  


**Browse Services by Category**

* As a patient, I want to browse available medical services by category (e.g., lab tests, imaging, consultations) so that I can quickly find what I need.  
* Priority: 1	  
* Estimate: Requires database of services as well as system to retrieve records based on user input through UI. Time spent to set up database and integrate search feature will be shared among several user tasks. Estimated 7.5 days total.  
  * Design core service database schema: 2 days  
  * Develop backend search for query processing and filtering: 3 days  
  * Build UI components for search and results: 2 days


**Search for Services by Location**

* As a patient, I want to search for services by name, city or zip in San Bernardino County so that I can easily locate the medical facilities I am looking for.  
* Priority: 1	  
* Estimate: Requires expansion of the service database and search functionality so users can filter services by location field. Estimated 5.5 days total.  
  * Extend service database with location fields: 1 day  
  * Add database query logic to support filtering by location: 2 days  
  * UI development for location search and results display: 2 days


**View Detailed Provider Information**

* As a patient, I want to view detailed provider information including name, phone, fax, address, website, hours of operation, and available services so that I have all the necessary details to make informed care decisions.  
* Priority: 1	  
* Estimate: Requires expansion of the service database with detailed provider information and creating a detail page to display the information to users. Estimated 3.5 days total.  
  * Extend database with additional provider information fields: 1 day  
  * UI for provider detail page layout: 2 days


**Create Account**

* As a user (patient, provider, or administrator), I want the option to create an account so that I can access features and role-specific tools.  
* Priority: 2  
* Estimate: Requires implementing user registration and login with role-based access, email verification, and secure password handling. Estimated 6.5 days total.  
  * Create a UI page for user account creation: 3 days  
  * Extend database with additional user fields: username, email, location of residence, etc: 3 days


**Ratings/Reviews**

* As a patient, I want to provide ratings or feedback on completed services so that I can share my experience with others and the hospital.  
* Priority: 2	  
* Estimate: Requires creation of reviews and ratings system linked to users, along with UI for displaying that feedback. Estimated 6.5 days total.  
  * Create reviews data model: 2 days  
  * UI for review submission form and review display: 2 days  
  * UI for administrator moderation controls: 2 days

**Provider Offerings**

* As a provider, I want to view the catalog of services offered in my facility so that I can recommend appropriate options to patients.  
* Priority: 1	  
* Estimate: Creating an alternate view of the catalogue specifically for providers. Estimated 3.5 days total.  
  * Filter services by provider/facility: 1 day  
  * UI for services specific to that facility: 2 days  
    


**Update Provider Offerings**

* As an administrator, I want to add, edit, or remove services in the catalog so that offerings remain accurate and up to date.  
* Priority: 1	  
* Estimate: Functionality for administrators to manage catalogue entries through adding, editing, or removing services through an administrator panel. Estimated 5.5 days total.  
  * Extend database logic to support create/update/delete operations: 1 day  
  * Implement backend logic to edit database according to management actions: 2 days  
  * UI for administrator panel: 2 days

**User Stories (Non-MVP)**  


**Search Based on Current Location**

* As a patient, I want to search for medical services by category (e.g., lab tests, imaging, consultations) based on my current location in San Bernardino County and view the fastest route on a map so that I can easily access nearby care options.  
* Priority: 3	  
* Estimate: Requires using browser location data and mapping integration through API call to filter services by proximity and display the fastest route. Estimated 6.5 days total.  
  * Setup browser geolocation: 1 day  
  * Extend query logic to filter services by proximity: 2 days  
  * Integrate with Google Maps API or something similar: 3 days

**Allow Administrators to Verify Status**

* As an administrator, I want to be able to verify the status of healthcare providers requesting access so that only legitimate providers can add or edit service details.  
* Priority: 3	  
* Estimate: Requires extending user profiles with credential fields, creating a submission process for documents, and letting admins approve or reject them. Estimated 5.5 days total.  
  * Extend user database with credential fields: 1 day  
  * UI for providers to upload proof: 2 days  
  * UI for administrator view to approve or reject: 2 days

**Compare Costs**

* As a patient, I want to check insurance coverage and out-of-pocket costs for each service so that I can make informed financial decisions.  
* Priority: 4	  
* Estimate: Requires extending the service database with pricing and insurance details, and a system for cost calculation. Estimated 5.5 days total.  
  * Extend service database with cost and insurance fields: 1 day  
  * Backend calculation for coverage and copay/deductible: 2 days  
  * UI for cost breakdown: 2 days

**Statistical Reporting for Administrators**

* As an administrator, I want to generate reports on service usage and demand so that I can make data-driven decisions.  
* Priority: 4	  
* Estimate: Requires storing and aggregating service usage data, and then creating admin reporting tools with visualization and export options. Estimated days 6.5 days total.  
  * Set up data analytics model: 3 days  
  * UI for admin report of statistics: 2 days  
  * Option to export data: 1 day

**Time Estimate Subtotal, MVP: 38.5**  
**Time Estimate Subtotal, non-MVP: 24**  
**Total Days: 62.5**

