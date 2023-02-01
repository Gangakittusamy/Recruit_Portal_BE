python -m virtualenv venv
------------------------
docker build -t recuirementportal-python . 
docker run -p 81:80  recuirementportal-python 80
-----
docker-compose up --build -d