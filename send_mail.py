import time

from models import User, Advertisement
from flask import jsonify, request
from app import app, celery
import errors
from flask.views import MethodView
from tasks import send_mail
from celery.result import AsyncResult


class SendMailView(MethodView):

    def post(self):
        emails = []
        if 'user_ids' in request.json:
            for id in request.json['user_ids']:
                email = User.query.get(id).email
                if email:
                    emails.append(email)
        else:
            raise errors.NotFound

        task = send_mail.delay(emails)
        return jsonify({'task_id': task.id})

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({'status': task.status,
                        'result': task.result})



