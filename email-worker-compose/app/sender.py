import psycopg2
import redis
import json
import os
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)

        db_name = os.getenv('DB_NAME', 'email_sender')
        db_user = os.getenv('DB_USER', 'postgres')
        db_host = os.getenv('DB_HOST', 'db')
        DSN = f'dbname={db_name} user={db_user} host={db_host}' # Data Source Name
        # DSN = 'dbname=email_sender user=postgres host=db' # Data Source Name
        self.conn = psycopg2.connect(DSN) # it makes the connection with the DATABASE

    def register_message(self, subject, message):
        SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)' # Structured Query Language
        cur = self.conn.cursor()
        cur.execute(SQL, (subject, message))
        self.conn.commit()
        cur.close()

        msg = {'subject': subject, 'message': message}
        self.fila.rpush('sender', json.dumps(msg))

        print('Registered Message !')

    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')

        self.register_message(subject, message) # Function [register_message]
        return 'Queued message ! Subject: {} Message: {}'.format(subject, message)

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)