
from flask_mail import Message
from flask import Blueprint, jsonify, request, session, redirect, url_for
from dotenv import load_dotenv
import os
import pytz


load_dotenv()
communication_blueprint = Blueprint("Communication", __name__)


@communication_blueprint.route("/sendMail", methods=["POST"])
def Send_mail():
    try:
        print("Process started.")
        from ..main import mail
        print("mail imported.")
        msg = Message(
            'Hello Sir',
            sender='mca120089@gmail.com',
            recipients=['uic.20mca1203@gmail.com']
        )
        print("mesg made.")
        msg.body = 'Hello Flask message sent from Flask-Mail'
        print("sending start")
        mail.send(msg)
        print("sended")
        return jsonify({'status': "failed", "code": 401, "msg": "Mail sended"})
    except Exception as e:
        print("Error(Send_mail) : Error occured : ", str(e))
