# README #


### What is this repository for? ###

* Quick summary
* Version 2.0
This repository is for a web app that displays prices of fuel in different companies in Ghana. It also exposes REST API endpoints to query/update the prices. It is written in Python, using the Django web framework.
This web app is currently running at http://fuelgh.com/
The API (Swagger UI) - http://fuelgh.com/swagger-ui/

### Who is this repository for? (Why become a Contributor) ###
Almost all consumer products have a way consumers can compare prices and buy what suits their budget. I believe there is the need to create an authoritative source that tracks the prices of crude oil products and help consumers make an informed decision when buying diesel/petrol.
If you share this belief, then kindly consider becoming a contributor.

### How do I get set up? ###

* Install docker-compose
* Enter the root of the project directory
* Run **docker-compose up**
* Enter a bash shell in the web service's container (fuelgh_web) and run **python manage.py migrate**
* Run **python manage.py createsuperuser** and follow the prompts to create a super user
* Run the tests **python manage.py test**
* Run **python manage.py reload_omcs** to get the latest prices
* Visit http://localhost:8000/

### How do I run it in production? ###
* Run **docker-compose up -f docker-compose.yml -f docker-compose.prod.yml -up -d --build**