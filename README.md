# README #


### What is this repository for? ###

* Quick summary
* Version 1.0
This app is currently running in open beta at http://fuelgh.com
This repository is for a web app that displays prices of fuel in different companies in Ghana. Written in Python, using the Django web framework. In the absence of a publicly available API to update the prices, we manually update the prices using an Excel sheet from http://www.npa.gov.gh/. (See "How do I get set up?"). 
There is the foundation for a basic REST API so we could possibly become that publicly available API for indicative prices for fuel in Ghana.

### Who is this repository for? (Why become a Contributor) ###
Almost all consumer products have a way consumers can compare prices and buy what suits their budget. I believe there is the need to create an authoritative source that tracks the prices of crude oil products and help consumers make an informed decision when buying diesel/petrol.
If you share this belief, then kindly consider becoming a contributor.

### How do I get set up? ###

* Create a virtualenv, activate it and install requirements from "requirements.txt" file using pip
Check out https://docs.python-guide.org/dev/virtualenvs/ for more instructions on the same
* Configure Database
Run "./manage.py migrate" and create a super user using "./manage.py createsuperuser"
* Modify username in "scrapeprices" command file
Open "fuelprices/management/commands/scrapeprices.py" and modify line 9 using the username created in the previous step.
* Import latest fuel data from http://www.npa.gov.gh/
Run "./manage.py scrapeprices" and input the current week's URL to the indicative prices. The URL at the time of this writing: http://www.npa.gov.gh/images/npa/documents/indicative-prices/2018/Indicative_Prices_for-_1st_-_15th_September_2018.xlsx
The current URL can be found at www.npa.gov.gh under the "Key documents" section. (Still working on a way of automating this)
* Deployment
With your virtualenv activated, run "./manage.py runserver" and observe your populated diesel and petrol prices in all their glory. Sortable by cheapest petrol and diesel.
