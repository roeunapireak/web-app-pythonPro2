from flask import (Flask, session, request, 
                   redirect, url_for)




def index():
    return "hello world"



app = Flask(__name__) 
# create rules
app.add_url_rule('/', 'index', index) 



if __name__ == "__main__":
    # Starting the web server:
    app.run()
