"""
This script runs the BlackHole application using a development server.
"""

from os import environ
from BlackHole import app

if __name__ == '__main__':
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '80'))
    #except ValueError:
    #    PORT = 5555
    #app.run(HOST, PORT)
    # website_url = 'vibhu:80' # -> add this "192.168.1.72       vibhu" to the hosts file on C:\Windows\System32\drivers\etc
    # app.config['SERVER_NAME'] = website_url  
    try:
        raise RuntimeError # comment this line for transmitting on your own network
        app.run(host='192.168.137.1',port=80,threaded=True,debug=False) # port 80 means http
    except:
        try:
            app.run(host='192.168.1.72',port=80,threaded=True,debug=False)
        except:
            app.run(host='127.0.0.1',port=80,threaded=True,debug=False)
