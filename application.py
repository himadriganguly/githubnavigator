import re
from cgi import escape

import os
import urllib.request
import json

# Jinja2 Template
from jinja2 import Environment, FileSystemLoader

# This will extract the template path for rendering
path = os.path.dirname(os.path.realpath(__file__))
tempPath = path + '/' + 'templates'
env = Environment(loader=FileSystemLoader(tempPath))


# This function will be mounted on "/" and display a entry link
def index(environ, start_response):
    '''
        This is the root of the application which is served when / is requested.
        When the browser request for the homepage of the application then
        Nginx receives the request and passes to WSGI Server (i.e uWSGI)
        WSGI Server exceutes the request and send the response
    '''

    # This is the web header send to the browser
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    # Jinja2 template file to be used
    template = env.get_template('index.html')

    # Render the template to the client after rendering the template
    return [template.render().encode('utf-8')]

def navigator(environ, start_response):
    '''
        This part of the Application will fetch the JSON data from the GitHub API
        based on the search keyword provided. Then extract the required field
        from the JSON data and send the data to Jinja2 Template for rendering.
    '''

    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    # set the template to be used
    template = env.get_template('search_result.html')

    # get the name from the url if it was specified there.
    args = environ['myapp.url_args']
    if args:
        keyWord = escape(args[0])
    else:
        return [template.render(theKey='None').encode('utf-8')]

    urlData = 'https://api.github.com/search/repositories?q=' + keyWord

    webUrl = urllib.request.urlopen(urlData)
    theData = []

    if(webUrl.getcode() == 200):
        data = webUrl.read()
        theJSON = json.loads(data.decode('utf-8'))

        total = theJSON['total_count']
        latest = 5 if total > 5 else total

        if total > 0:
            for i in range(0,latest):
                description = theJSON['items'][i]['description']
                repoName = theJSON['items'][i]['name']
                createdAt = theJSON['items'][i]['created_at']
                ownerUrl = theJSON['items'][i]['owner']['html_url']
                avatarUrl = theJSON['items'][i]['owner']['avatar_url']
                ownerLogin = theJSON['items'][i]['owner']['login']

                repoUrl = theJSON['items'][i]['html_url']

                commitsUrl = theJSON['items'][i]['commits_url']
                commitsUrl = commitsUrl[0:-6]

                try:
                    commitJSON = urllib.request.urlopen(commitsUrl)

                    if(commitJSON.getcode() == 200):
                        commitData = commitJSON.read()
                        commitJSONData = json.loads(commitData.decode('utf-8'))
                        commitSha = commitJSONData[0]['sha']
                        commitMessage = commitJSONData[0]['commit']['message']
                        committerName = commitJSONData[0]['commit']['committer']['name']
                    else:
                        commitSha = 'Data Cannot Be Loaded'
                        commitMessage = 'Data Cannot Be Loaded'
                        committerName = 'Data Cannot Be Loaded'
                except:
                    commitSha = 'Data Cannot Be Loaded'
                    commitMessage = 'Data Cannot Be Loaded'
                    committerName = 'Data Cannot Be Loaded'

                theData.append({'search_term': 'arrow', 'respository_name': repoName,\
                            'created_at': createdAt, 'owner_url': ownerUrl,\
                            'avatar_url': avatarUrl, 'owner_login': ownerLogin,\
                            'sha': commitSha, 'commit_message': commitMessage,\
                            'commit_author_name': committerName,\
                            'repository_description': description,\
                            'repository_url': repoUrl})

            # sorts the data based on created_at in decending order
            theData = sorted(theData, key=lambda k: k['created_at'], reverse=True)

            # return the response with the template
            return [template.render(theKey=keyWord, theDatas=theData, total=total,\
                                latest=latest).encode('utf-8')]
        else:
            return [template.render(theKey='Not Found').encode('utf-8')]
    else:
        data = "Received an error from server cannot retrieve results. " +\
                str(webUrl.getcode())
        return [template.render(test=data).encode('utf-8')]

def not_found(environ, start_response):
    '''
        Called if no URL matches.
    '''

    status = '404 Not Found'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    # set the template to be used
    template = env.get_template('404.html')

    return [template.render().encode('utf-8')]

# map urls to functions
urls = [
    (r'^$', index),
    (r'^navigator/$', navigator),
    (r'^navigator/(?:search_term=(?P<term>.+))?$', navigator),
]


def application(environ, start_response):

    urlPath = environ.get('PATH_INFO', '').lstrip('/')

    if(urlPath != '' and urlPath[-1] != '/'):
        urlPath += '/'
    if(environ.get('QUERY_STRING', 'none') != 'none'):
        urlPath += environ.get('QUERY_STRING', '')

    for regex, callback in urls:
        match = re.search(regex, urlPath)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return callback(environ, start_response)

    return not_found(environ, start_response)


if __name__ == '__main__':

    try:
        print("*****************************************************************************\n")
        print('             GitHub API Search Application\n')
        print('              Developed by Himadri Ganguly\n')
        print('            https://github.com/himadriganguly\n')
        print('   WSGI Application using Python3, Gunicorn, Nginx\n')
        print("*****************************************************************************\n")
        print("             Starting Server on port 9876...\n")
        print("   Open browser and go to http://localhost:9876 to use the application\n")
        print("           You can also do GET request to e.g.\n")
        print("        http://localhost:9876/navigator?search_term=arrow\n")
        print("*****************************************************************************\n")
        os.system("uwsgi uwsgi.ini")
    except Exception as e:
        print('Error Occured' + e)
    except KeyboardInterrupt as e:
        print('Shutting Down Server!')
