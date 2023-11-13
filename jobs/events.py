from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session, abort, request

from time import time

socketio = SocketIO()

@socketio.on('connect')
def connect():
    print('Connected!!!')
    print(session)
    # job_id = session.get('jobID')
    # if job_id is None:
    #     abort(404)

    # join_room(job_id)
    # obj = requests.get(f'localhost:5000/jobs/{job_id}')
    # emit('joined', obj.json(), room=job_id)


@socketio.on('startJob')
def start_job():

    job_id = session.get('jobID')
    if job_id is None:
        abort(404)

    join_room(job_id)
    emit('startedJob', {}, room=job_id)


@socketio.on('close')
def _leave_room():

    job_id = session.get('jobID')
    if job_id is None:
        abort(404)

    leave_room(job_id)


@socketio.on('postComment')
def _post_comment(value: dict):
    print('posting comment')

    emit('emitComment', {'text' : value['text'], 'timestamp' : time() * 1000}, broadcast=True, include_self=False)
