port 8000 for debug
port 8080 for production

docker-compose -f docker-compose.yml up --build
docker-compose build -> docker-compose up

To create supersuser, navigate to the /app directory and type the following command:
    python manage.py createsuperuser

In /app:
    ./manage.py test appvocado/tests/

    ./manage.py test appvocado.tests.unit_tests.test_general


