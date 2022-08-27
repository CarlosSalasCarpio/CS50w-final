# Human Resources Document Management System (final project CS50w)

For my final project for CS50's web programming with Python and Javascript, I decided to create a Document Management System intended to be used by Human Resources teams.

## Overview

### The problem

There are probably hundreds or thousands of small companies out there that require to automate their processes but lack the resources to buy an enterprise-level solution.

Some months ago I get with a small engineering company with a human resources department struggling to manage their documentation for their 100-plus employees.

The team of two people was dependent on Excel spreadsheets and a lot of patience to one by one create these documents for each of their employees on request.

Having completed CS50X and been in the middle of CS50's web Programming with Python and Javascript, I decided to ta tackle this problem, and after a couple of meetings with the human resources of the company, we identified the following requirements for the tool.

The platform should be able to:

1. Have a register, login, logout, and password reset system
2. Have staff accounts for the human resources team and standard accounts for the employees of the company
3. Have a staff interface where the employees' information can be uploaded using a .CSV file
4. The staff interface should also have a way to upload and store employee's payroll certificates (.PDF files)
5.  The employees should be able to download employment verification letters automatically generated from the information taken from the .CSV file
6. The user should be able to download payroll certificates previously uploaded by the human resources team.
7. The application must be mobile-responsive.

***I developed this platform completely by myself with the only purpose of applying the concepts learned in CS50, so even though this was developed for a small company I didn't receive any kind of help from a third party.**

### The tech stack

1. For the back-end I used Django.
2. For the front-end, I used Javascript and bootstrap
3. For the database, I used PostgreSQL**
4. For the deployment of the application, I used Azure App Services**
5. To store the payroll certificates I used Azure Storage**

****This was implemented for the final platform delivered to the company, for the version of the platform showcased for CS50 I kept with SQLite and local storage, also, this version was not deployed so it runs locally.**

### The solution

#### User authentication

Django has some pre-built libraries that are pretty helpful for user [authentication](https://docs.djangoproject.com/en/4.0/topics/auth/default/). This allows to easily create a login, logout, and register similar to most CS50's projects.

I started by creating a NewUserForm, in my case, I kept the Django default fields, also, I kept the default structure for the login and logout functions.

Also for the password reset functionality, I used the standard Django authentication system and just customized the HTML templates for each route ```password_reset.html```,  ```password_reset_sent.html```, ```password_reset_form.html``` and ```password_reset_done.html```.

#### Admin dashboard

If the user that logs in to the application has a staff account (therefore is part of the human resources team), he will be presented with a specific user interface that allows him to manage the employees' information stored in the application, and to store and manage documentation that the employee should download on a monthly basis.

The staff users have two features available, they can either upload a .csv file (by clicking on the option "Employees") or a .pdf file (by clicking on the option "Certificates"), the .csv file has all the employee's information while the. pdf files are payroll certificates that are stored by the application so the employees can download them as requested.

![Screenshot 2022-08-14 130247.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1660500189890/Q80LBB3rO.png align="left")

This dashboard works as a single-page application, the different features are shown and hidden using Javascript. The functions created for this are available on ```admin.js```

##### Managing employees

If a staff user is in the "Admin dashboard" and clicks on "Employees", he will be redirected to a form that allows him to select a .CSV file in order to update the employees' database.

This .CSV file contains information like the employee's full name, document type, ID, monthly salary, and hiring date among others.

When the user selects a file and clicks on "Update", the server sends a POST request to ```/admin_main```, then the following validations and custom functions are executed:

1. Check that the form is valid and that the file is a .CSF file. If the file is not a .CSV file the user will be presented with an error asking to verify the file's extension.
2. If the form and the document's extension are valid, the .CSV file is decoded and read.
3. Then, the custom function ```csv_to_models``` located in ```utils.py``` is executed. This function first deletes all the existing entries in the model ```Employees``` (if any) and then starts populating the ```Employees``` module with the entries available in the .CSV file.
4. Finally, if the employees' information is correctly updated, the user will receive a message "Employees' information successfully updated".

##### Managing payroll certificates

If a staff user is in the "Admin dashboard" and clicks on "Certificates", he will be redirected to a form that allows him to select a .PDF file in order to upload it to the platform.

The form shown to the user has 3 char fields "fortnight", "month" and "year" and the "pdf" field which is a file field, the three first fields define the term to which the document selected belongs (let's say for example the first half o August of 2022), the three first fields are selected by the user from a drop-down list.

When the user fills out the form, selects a file, and clicks on "Upload", the server sends a POST request to ```/admin_main```, then the following validations and functions are executed within the view:

1. Check that the form is valid and that the file is.PDF file. If the file is not a .PDF file the user will be presented with an error asking to verify the file extension.
2. If the form is valid and the file extension is .PDF, but, there is an existing file for the term indicated (same month, year, and fortnight) the user will be presented with an error "The file you are trying to upload already exists, if you want to replace the existing file, please first delete the existing one".
3. If the form and the document's extension are valid, the form is saved, and the document is stored, in the full version of the application, it is sent to an Azure Storage Account, however, on the version for CS50 it is stored in the folder /media.
4. Finally, if the employees' information is correctly updated, the user will receive a message "The document was successfully uploaded".

###### Download payroll certificate

If the staff member clicks on the "download" option on an existing payment certificate, a POST request is sent with the primary key of the specific payment certificate to be downloaded ```/download_desprendible```, the route where the PDF is stored is retrieved, and then the document is downloaded using the pre-built Django function ```FileResponse```

###### Delete payroll certificate

If the staff member clicks on the "delete" option on an existing payment certificate, a POST request is sent with the primary key of the specific payment certificate to be deleted ```/delete_desprendible```, then the payment certificate is retrieved ```desprendible = Desprendibles.objects.get(pk = pk)``` and deleted ```desprendible.delete()```

#### User's dashboard

If the user that logs in to the application is not a staff user (therefore a company's employee), he will be presented with a specific user interface that allows him to download payroll certificates or to generate employment verification letters.

![Screenshot 2022-08-15 111515.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1660580131050/Afpht0GO4.png align="left")

##### Download employment verification letters

If the user clicks on the "download job certificate" option, a POST request is sent to ```/download_certificado_user```. The view ```download_certificado_user``` executes the following actions to generate and download the employment verification letter:

1. The employees' information is retrieved, this includes full name, document type, id, hiring date, role, contract type, salary, and company name.
2. The employee's information together with some additional information such as the system date and company logos is sent as context to fill an HTML template ```certificado.html```
3. The HTML template is rendered and downloaded as a .PDF file ([I have an entire article describing this process on Hashnode](https://carlosenriquesalas.hashnode.dev/html-template-to-pdf-in-django))

##### Download payroll certificate

If the user clicks on the "download" option on an existing payment certificate, a POST request is sent with the primary key of the specific payment certificate to be downloaded ```/download_desprendible```, the route where the PDF is stored is retrieved, and then the document is downloaded using the pre-built Django function ```FileResponse```

## Models

The application has 3 models in total:

1. ```Users``` - Default Django model for users
2. ```Employees``` - This model stores the employees' personal information, including employee's name, surname, ID, and monthly salary, among others (it has a total of 41 fields containing employee's information)
3. ```Desprendibles``` - This model ("desprendibles" is Spanish for payroll certificate) maps the .pdf files uploaded by the staff users, it has 4 fields, "fortnight", "month", "year" and "pdf", the first three indicates the period of time corresponding to each payment certificate (the employees of this company are paid every 15 days, so every 15 days the HR team uploads a new certificate, there cannot be two certificates for the same period of time). The final field "pdf" maps the URL (or for the CS50's version the directory) where the .pdf file is stored, in the full version of the application it is sent to an Azure Storage Account, however, on the version for CS50w it is stored in the folder /media

## Routes

The following routes were created for this project:

1. Index - ```/``` - This is the employees' main page, from here they can download their payroll certificates or employment verification letters
2. Login - ```/login``` - User's who have a valid username and password can log in to the platform
3. Logout - ```/logout``` - Logout
4. Register - ```/register``` - Users who are included within the platform via the .CSV file uploaded by the staff member can register to the platform, if a user tries to register to the platform using an id not previously registered by the staff personnel, they will be presented with an error
5. Admin dashboard - ```/admin_main``` - From here the staff members have access to the staff features (manage payroll certificate and employment verification letters)
6. Delete a payment certificate - ```/delete_desprendible``` - From here a staff member can delete a payment certificate previously uploaded to the platform
7. Download payment certificate - ```/download_desprendible``` - From here either an employee or a staff member can download a payment certificate
8. Download employment verification letter - ```/download_certificado_user``` - From here an employee can download a employment verification letter
9. Initiate reset password process -```/reset_password``` - Allows users to reset their paswword
10. reset_password_sent ```/reset_password_sent``` - Confirms that a recovery password link has been sent to the user's email
11. Index ```/reset/<uidb64>/<token>``` - When a user opens the recovery link, is presented with a reset form
12. Index ```/reset_password_complete``` - Confirms that the password has been recovered successfully