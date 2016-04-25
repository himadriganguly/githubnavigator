# GitHub Navigator :mag:

It is a small Python Web Application which supports WSGI (Web Server Gateway Interface) to search GitHub Repository using search keyword. The application fetches the result using the GitHub Search API ([https://developer.github.com/v3/](https://developer.github.com/v3/)) and display the latest 5 results and sorts them in decending order based on the Creation Date of the Repository. It displays results such as Creation Date, Author, Description, Last Commit etc in a besutiful presentation. Two version of the application is develop to utilize [**Gunicorn**](http://gunicorn.org/) and [**uWSGI**](https://github.com/unbit/uwsgi) with [**NGINX**](http://nginx.org/) server.


## Requirements

1. Python3
2. PIP3
3. Virtualenv
4. uWSGI        - 2.0.12
5. Gunicorn     - 19.4.5
6. Jinja        - 2.8
7. NGINX        - 1.9.15


## Application ScreenShot

![GitHub Navigator](https://raw.githubusercontent.com/himadriganguly/githubnavigator/master/screenshots/screenshot.jpg "GitHub Navigator Search Result Preview")


## Running The Application

1. You should have Python3 installed on your system
2. Install PIP3 using `sudo apt-get install python3-pip`
3. Install Virtualenc using `pip install virtualenv`
4. Now create a virtual environment using `virtualenv -p [path to your python3] [name of the virtual environment]`
5. Activate the virtial environment by using `source [path to your virtual environment]/bin/source` [Note:- To deactivate just type `deactivate`]
6. Install uWSGI using `pip install uwsgi`
7. Install Gunicorn using `pip install gunicorn`
8. Install Jinja2 using `pip install Jinja2`
9. NGINX should be installed in your system
10. Download the application from GitHub -
11. Extract the application
12. Copy the `www` folder within the `extras` folder to `/home/`
13. If you like to use **uWSGI** then copy `localhost.conf` file within `extras` to `conf.d` folder of NGINX
14. If you like to use **Gunicorn** then change the filename of `localhost.gunicorn.conf` to `localhost.conf` file within `extras` to `conf.d` folder of NGINX
15. Start NGINX using `sudo service nginx start`
16. If you like to use **uWSGI** then move to the folder where you have extracted the application in `terminal` and then run `python application.py`. To stop the server press `CTRL+C`. [Note:- Virtual environment should be activated before this]
17. Now you can check out the application at `http://localhost:9876` or you can directly use the search feature of the application using `http://localhost:9876/navigator?search_term=[search keyword]` replace [search keyword] with your own keyword and you will get the result.
18. If you like to use **Gunicorn** then move to the folder where you have extracted the application in `terminal` and then run `python application.gunicorn.py`. To stop the server press `CTRL+C`. [Note:- Virtual environment should be activated before this]
19. Next process remains the same as above [No. - 17]
20. ENJOY :thumbsup: :beer:


## Other Tools Used

1. Git (For source code management) [**https://git-scm.com/**](https://git-scm.com/)


## Features

1. Search GitHub Repository and fetches result using GitHub API and display result in beautiful format
2. The Homepage provides a Form to enter your search keyword `http://localhost:9876`
3. You can also directly access URL with the search keyword and get the result `http://localhost:9876/navigator?search_term=[search keyword]`
4. The application uses the WSGI concept to serve the application
5. NGINX is used as the Web Proxy which receives the request from the client and forwards it to Gunicorn or uWSGI
6. Gunicorn and uWSGI serves as the HTTP server and servers the response to NGINX server
7. NGINX receives the response and fetches the static files such as css, js etc and serves the page to the client
8. Twitter Bootstrap is used to get Responsive Layout so that it fits all screen


## CONTRIBUTE

If you have any idea you want to implement in this project please do so or if you want to make the code better please go ahead and make a pull request, I will try my best to merge appropriately.

Hope you will like the application. CHEERS :beer:
