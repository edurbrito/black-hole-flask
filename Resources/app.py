from flask import Flask, render_template
import config as cfg
app = Flask(__name__)
app.config.from_object(cfg.Config)

@app.route('/')
@app.route('/index.html')
@app.route('/home')
def index():
    
    return render_template('index.html')

if __name__ == '__main__': 
    # website_url = 'vibhu:80' # -> add this "192.168.1.72       vibhu" to the hosts file on C:\Windows\System32\drivers\etc
    # app.config['SERVER_NAME'] = website_url  
    import socket
    host = str(socket.gethostbyname(socket.gethostname()))
    print(host)
    try:
        raise RuntimeError # comment this line for transmitting on your own network
        app.config['SERVER_NAME'] = "mensagemdecoded.pt"
        host = '192.168.137.1'
        app.run(host=host,port=80,threaded=True,debug=False) # port 80 means http
    except:
        try:
            app.run(host=host,port=80,threaded=True,debug=False)
        except:
            app.run(host='127.0.0.1',port=80,threaded=True,debug=False)
