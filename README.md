## Info
When running the project, you can access the search engine (I recommend Chrome) and interact and visualize the API.
The complete documentation will be attatched next to this ZIP folder.
In addition, a Postman collection will be attatched so it is easier to test the API.
The specification is in the file generated_yaml.yaml in the root directory. For easier understanding I recommend pasting its contents into the Swagger editor.

## Run the program with Docker
It is needed to install Doker in the computer to run this project.
    This tutorial is very helpful: https://docs.docker.com/desktop/windows/install/
After it is installed, you need to run it.
To run the docker files, from the root directory use one of the two commands:
    docker-compose -f docker-compose.yml up --build
    docker-compose build -> docker-compose up

# Requirements
The list of requirements needed to install are in the requirements.txt file in the root folder. When running this project by Docker, these are already installed in the image.
    Django>=3.0.6,<3.1
    uWSGI>=2.0.18,<2.1
    djangorestframework==3.13.1
    Pillow==8.4
    dj_rest_auth
    django-allauth
    djangorestframework-simplejwt


# Run tests
To run the tests, first we need the backend running. Use the same command as mentioned before.
After, navigate to the /app directory and type the following command to test each test file individually:

    ./manage.py test appvocado.tests.unit_tests.<name_of_file>
    
    for example:
        ./manage.py test appvocado.tests.unit_tests.test_general

If there is authentication problems, make sure the cookies are deleted. The same happens in the Postman collection.

## Create superuser
To create supersuser, navigate to the /app directory and type the following command:
    python manage.py createsuperuser