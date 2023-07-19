import random

from flask import Flask
from celery import Celery

app = Flask(__name__)
worker = Celery('worker',
                broker='amqp://admin:mypass@rabbit:5672',
                backend='rpc://')


@app.route('/simple/task')
def call_method():
    app.logger.info("Invoking Method ")
    r = worker.send_task('tasks.calculator', kwargs={'x': random.randrange(0, 10, 1), 'y': random.randrange(0, 10, 1)})
    app.logger.info(r.backend)
    return r.id


@app.route('/simple/task/<task_id>')
def get_status(task_id):
    status = worker.AsyncResult(task_id, app=worker)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/simple/task/result/<task_id>')
def task_result(task_id):
    result = worker.AsyncResult(task_id).result
    return "Result of the Task " + str(result)
