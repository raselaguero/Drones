Username: admin
Password: admin123*

Compilation
1- Install and run the xampp application
2- Change the default http port to 81 or 90
3- Modify the httpd.conf file
-	Listen 81
-	WSGIPythonPath /root_to_app
- Create a virtual host with the absolute address of the application
Example:
<VirtualHost *:81>
	ServerName messanger-drones.com
	ServerAdmin admin@gmail.com
	LogLevel warn
	WSGIScriptAlias / / file address wsgi.py
</VirtualHost>
4- Modify the project settings file
- change variable DEBUG = False
- change SECRET_KEY to an environment variable
- rename the database with the absolute path to the “.db” file
- change variable STATIC_URL = 'http://localhost:81/static/'
5- Click on the Start button of Apache
Execution
You can manage the file from the project API at the following addresses
1- Register a drone: http://messanger-drones.com/messanger/drones/
2- Load a drone with medications: http://messanger-drones.com/messanger/medications/ 
Note: JSON Parser don’t support file uploads. https://www.django-rest-framework.org/api-guide/fields/#file-upload-fields. I solved it excluding image in the AFTER and depositing image with the method PATCH with MultiPartParser.

3- Update a drone with medications (PUT, PATCH): http://messanger-drones.com/messanger/medications/7/ 
4- Check the medications loaded for a given drone: http://messanger-drones.com/messanger/drones/14/ 
5- Check the drones available for loading: http://messanger-drones.com/messanger/drones/available-loading/ 
6- Check the drone battery level for a given drone: http://messanger-drones.com/messanger/drones/14/battery-level/

7- Register a subscriptor: http://messanger-drones.com/messanger/emails/
8- Update a subscriptor: http://messanger-drones.com/messanger/emails/2/


Proof
Django provides a test framework with a small hierarchy of classes that build on the Python standard unittest library.
1- Structure of the tests
Example: Messenger/
/tests/
__init__.py
test_models.py
test_forms.py
test_views.py
2- Run the tests
- In general: python3 manage.py test
- Specifically: python3 manage.py test Messenger.tests.test_models

NOTE: 
-	must edit the variable EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in the settings
-	you may need to go to your gmail and change setting to allow less secured app

