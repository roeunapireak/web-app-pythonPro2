
import sqlite3
from random import randint
 
db_name = 'quiz.sqlite'
conn = None
cursor = None

def open_session():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close_session():
    cursor.close()
    conn.close()

def execute_query(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    '''drop all tables'''
    open_session()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    execute_query(query)
    query = '''DROP TABLE IF EXISTS question'''
    execute_query(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    execute_query(query)
    close_session()


def create_db_objects():
    open_session()
    cursor.execute('''PRAGMA foreign_keys=on''')
    
    execute_query('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR)''' 
    )
    execute_query('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR, 
                wrong3 VARCHAR)'''
    )
    execute_query('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''
        )
    close_session()

def to_show(table):
    query = 'SELECT * FROM ' + table
    open_session()
    cursor.execute(query)
    print(cursor.fetchall())
    close_session()

def show_tables():
    to_show('question')
    to_show('quiz')
    to_show('quiz_content')


def add_questions():
    questions = [
        ('How many months in a year have 28 days?', 'All', 'One', 'None','Two'),
        ('What will the green cliff look like if it falls into the Red Sea?', 'Wet', 'Red', 'Will not change', 'Purple'),
        ('Which hand is better to stir tea with?', 'With a spoon', 'Right', 'Left', 'Any'),
        ('What has no length, depth, width, or height, but can be measured?', 'Time', 'Stupidity', 'The sea','Air'),
        ('When is it possible to draw out water with a net?', 'When the water is frozen', 'When there are no fish', 'When the goldfish swim away', 'When the net breaks'),
        ('What is bigger than an elephant and weighs nothing?', 'Shadow of elephant','A balloon','A parachute', 'A cloud')
    ]

    open_session()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close_session()

def add_quiz():
    quizes = [
        ('Quiz 1', ),
        ('Quiz 2', ),
        ('Quiz- do not understand which', )
    ]
    open_session()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close_session()


def add_links():
    open_session()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Add a link (y/n)?")

    while answer != 'n':
        quiz_id = int(input("quiz id: "))
        question_id = int(input("question id: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Add a link (y/n)?")

    close_session()

def get_question_after(last_id=0, vict_id=1):
    '''returns the next question after the question with the passed ID
    for the first question, the default value is passed'''
    open_session()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id] )
 
    result = cursor.fetchone()
    close_session()
    return result 

def get_quises():
    '''returns a list of quizzes (id, name) 
    you can only take quizzes in which there are questions, but so far a simple option'''
    query = 'SELECT * FROM quiz ORDER BY id'
    open_session()
    cursor.execute(query)
    result = cursor.fetchall()
    close_session()
    return result

def get_quiz_count():
    "' optional function '"
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open_session()
    cursor.execute(query)
    result = cursor.fetchone()
    close_session()
    return result

def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open_session()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close_session()
    return rand_id


def main():
    clear_db()
    create_db_objects()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    # print(get_question_after(0, 3))
    # print(get_quiz_count())
    # print(get_random_quiz_id())
    pass

if __name__ == "__main__":
    main()
