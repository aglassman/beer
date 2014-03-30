beer
====

A simple ReST service to manage Milwaukee's favorite beverages.


Install
=======

**pre-requisites:**  
Linux based OS, developed on:

Linux version 2.6.32-5-686 (Debian 2.6.32-48squeeze4) (dannf@debian.org) (gcc version 4.3.5 (Debian 4.3.5-4) ) #1 SMP Mon Sep 23 23:00:18 UTC 2013 

Python 2.6.5 or higher.


Install the following packages.
------------------------------

**Install pip:**  
	wget "https://raw.github.com/pypa/pip/master/contrib/get-pip.py" --no-check-certificate  
	sudo python get-pip.py  


**Install PostgreSQL:**  
	sudo apt-get install postgresql  

**Create database:**  
	sudo su postgres  
	createdb beer  
	psql beer  
	\password admin  
	(enter password)  

**Install connectors:**  
	sudo apt-get install libpq-dev python-dev  
	sudo pip install psycopg2  

**Install Django:**  
	sudo pip install Django==1.6.2  

**Install Apache:**  
	sudo apt-get install apache2  
	sudo apt-get install libapache2-mod-wsgi  

**Install Git:**  
	sudo apt-get install git  

**Install [Django ReST framework](http://www.django-rest-framework.org/):**  
	sudo pip install djangorestframework  
	sudo pip install markdown  
	sudo pip install django-filter  

**Install [Django Extensions](https://github.com/django-extensions/django-extensions):**  
	sudo pip install django-extensions  

**Install Django Filter**
	sudo pip install django-filter

---

Clone code from GitHub.
----------------------

Create user for the project.

	adduser beer

Navigate to user's home directory.
	
	cd /home/beer

Pull code from GitHub

	git clone https://github.com/aglassman/beer.git

Change permissions on beer directory.

	chmod 755 beer



Configure  apache2 server.
-------------------------

add the following to httpd.conf, then restart server.

NOTE: If apache version is pre 2.4.x, use 'Allow from all' rather than 'Require all granted'

	NameVirtualHost *:80

	WSGIPythonPath /home/beer/beer/django_beer

	<VirtualHost *:80>
	    UseCanonicalName Off
	    ServerAdmin  webmaster@localhost
	    DocumentRoot /var/www
	    
		WSGIPassAuthorization On

	    Alias /robots.txt /home/beer/beer/django_beer/static/robots.txt
	    Alias /favicon.ico /home/beer/beer/django_beer/static/favicon.ico

	    AliasMatch ^/([^/]*\.css) /home/beer/beer/django_beer/static/styles/$1

	    Alias /media/ /home/beer/beer/django_beer/media/
	    Alias /static/ /home/beer/beer/django_beer/static/

	    <Directory /home/beer/beer/django_beer/static>
	        Order deny,allow
	        Allow from all
	        Options FollowSymLinks
	    </Directory>

	    <Directory /home/beer/beer/django_beer/media>
	        Order deny,allow
	        Allow from all
	    </Directory>

	    WSGIScriptAlias /beer_api /home/beer/beer/django_beer/django_beer/wsgi.py

	    <Directory /home/beer/beer/django_beer/django_beer>
	        <Files wsgi.py>
	            Order deny,allow
	            Allow from all
	        </Files>
	    </Directory>
	</VirtualHost>

Create sym links for admin static files.
---------------------------------------
cd /home/beer/beer/django_beer/static 

sudo ln -s '/usr/local/lib/{python_version}/dist-packages/django/contrib/admin/static/admin' admin

sudo ln -s '/usr/local/lib/python2.6/dist-packages/rest_framework/static/rest_framework' rest_framework


Configure database connection.
-----------------------------
If needed, configure the database connection settings.

/home/beer/beer/django_beer/django_beer/settings.py

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	        'NAME': 'beer',
	        'USER': 'admin',
	        'PASSWORD': 'admin',
	        'HOST': 'localhost',
	        'PORT': '5432',
	    }
	}

