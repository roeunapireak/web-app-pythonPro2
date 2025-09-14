from flask import (Flask, session, request, 
                   redirect, url_for)

from db_script import get_question_after, get_quises, main 

main()

def start_quis(quiz_id):
    '''creates the desired values in the session dictionary'''
    session['quiz'] = quiz_id
    session['last_question'] = 0



def index():
    '''First page: if it came with a GET request, then choose a quiz, 
    if POST, then remember the quiz ID and send it to the questions'''

    if request.method == 'GET':
        start_quis(-1)
        return quiz_form()



app = Flask(__name__) 
# create rules
app.add_url_rule('/', 'index', index) 



if __name__ == "__main__":
    # Starting the web server:
    app.run()
