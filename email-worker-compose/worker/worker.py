import redis
import json
import os
from time import sleep
from random import randint

if __name__ == '__main__': # Test if this is the main archive that is bein running
    redis_host = os.getenv('REDIS_HOST', 'queue')
    r = redis.Redis(host=redis_host, port=6379, db=0)
    print('Waiting Messages...')
    while True:
        message = json.loads(r.blpop('sender')[1])
        # Send E-mail Simulate
        print('Sending message:', message['subject'])
        sleep(randint(15, 45))
        print('Message', message['subject'], 'Sent')