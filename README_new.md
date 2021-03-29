# README #


### What is this repository for? ###

* Quick summary
* Version 2.0
This app is currently running in open beta at http://fuelgh.com
This repository is for a web app that displays prices of fuel in different companies in Ghana. Written in Python, using the Django web framework. In the absence of a publicly available API to update the prices, we manually update the prices using an Excel sheet from http://www.npa.gov.gh/. (See "How do I get set up?"). 
There is the foundation for a basic REST API so we could possibly become that publicly available API for indicative prices for fuel in Ghana.

### Who is this repository for? (Why become a Contributor) ###
Almost all consumer products have a way consumers can compare prices and buy what suits their budget. I believe there is the need to create an authoritative source that tracks the prices of crude oil products and help consumers make an informed decision when buying diesel/petrol.
If you share this belief, then kindly consider becoming a contributor.

### How do I get set up? ###

* Install docker-compose
* Enter the root of the project directory
* Run **docker-compose up**
* Enter a bash shell in the web service's container (fuelgh_web) and run **python manage.py migrate**
* Run **python manage.py createsuperuser** and follow the prompts to create a super user
* Run **python manage.py reload_omcs** to get the latest prices
* Visit http://localhost/
