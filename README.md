port 8000 for debug
port 8080 for production

To run the docker files, from the root directory use one of the two commands:
    docker-compose -f docker-compose.yml up --build
    docker-compose build -> docker-compose up

To create supersuser, navigate to the /app directory and type the following command:
    python manage.py createsuperuser

To run the tests, first we need the backend running. Use the same command as mentioned before.
After, navigate to the /app directory and type the following command to test each test file individually:

    ./manage.py test appvocado.tests.unit_tests.<name_of_file>
    for example:
    ./manage.py test appvocado.tests.unit_tests.test_general


