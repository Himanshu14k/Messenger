from nis import cat
from projectModule.authentications.userAuthApi import GetMeetsId
from projectModule.constants.http_status_code import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED, HTTP_417_EXPECTATION_FAILED


try:
    from flask import Blueprint, jsonify, request, session, redirect, url_for
    from projectModule.dbOperations.mongoOP import MongoDBManagement
    from dotenv import load_dotenv
    import bcrypt
    from datetime import datetime, timedelta
    from projectModule.commonOperations import sendOtpOnPhone
    import os
    import jwt
    import uuid
    from bson import ObjectId
    import pytz
    from flask_mail import Message
    from flask_jwt_extended import create_access_token, create_refresh_token
except Exception as e:
    print("Modules are Missing : {} ".format(e))


load_dotenv()
videoRooms_blueprint = Blueprint("VideoRooms", __name__)

@videoRooms_blueprint.route("/createR", methods=["POST"])
def CreateMeetRoom():
    """
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            
            m_id = InsertInVR(data)
            if InsertInUserCollection(m_id, data['invities'], data['uId']) == True:
                return jsonify({'status': "success", "code": 401, "msg": "Meeting created successfully!"})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Failed to create meeting link."})
        return jsonify({"status": "failed", "code": 401, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error (CreateMeetRoom): Error occured during meeting room creation.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


def InsertInVR(data):
    try:
        temp = {}
        id = uuid.uuid4().hex
        temp['_id'] = id
        temp['m_link']=''
        temp['status']=1
        temp['metting_info'] = {
            "time_s":data['time_s'],
            "time_e":data['time_e'],
            "date":data['date'],
            "m_title":data['m_title'],
            "type":data['type']
        }
        temp['invities']=data['invities']
        temp['created_by']=data['created_by']
        temp['created_at'] = datetime.now(pytz.timezone('Asia/Kolkata'))
        mongo = MongoDBManagement(
            os.getenv("USERID"), os.getenv("PASSWORD"))
        mongo.insertRecord(db_name="Communication_App",
                           collection_name="Video_Rooms", record=temp)
        return id
    except Exception as e:
        print("Error is : ", str(e))

def InsertInUserCollection(meet_Id, invities, uId):
    try:
        mongo = MongoDBManagement(
            os.getenv("USERID"), os.getenv("PASSWORD"))
        mongo.updateMultipleRecord(db_name="Communication_App",
                           collection_name="Users", query={
                            "_id": {"$in": invities}
                           }, newVal={
                            "$push":{"invitation_meetsId":meet_Id}
                           })
        mongo.updateMultipleRecord(db_name="Communication_App",
                           collection_name="Users", query={
                            "_id": uId
                           }, newVal={
                            "$push":{"orgainzer_meetsId":meet_Id}
                           })
        return True
    except Exception as e:
        print("Error is : ", str(e))

def GetOrgainizerMeet(ids):
    try:
        mongo = MongoDBManagement(
            os.getenv("USERID"), os.getenv("PASSWORD"))
        data = mongo.findRecordOnQuery(db_name="Communication_App",
                           collection_name="Video_Rooms", query={
                            "_id": {"$in": ids}
                           })
        return data
    except Exception as e:
        print("Error is : ", str(e))

def GetInvitationMeets(ids):
    try:
        mongo = MongoDBManagement(
            os.getenv("USERID"), os.getenv("PASSWORD"))
        data = mongo.findRecordOnQuery(db_name="Communication_App",
                           collection_name="Video_Rooms", query={
                            "_id": {"$in": ids}
                           })
        return data
    except Exception as e:
        pass


@videoRooms_blueprint.route("/getR", methods=["GET"])
def GetVideoRooms():
    """
        """
    try:
        if request.method == "GET":
            id = request.args.get('id')
            meets_Id = GetMeetsId(id)
            OrgainizerMeets = GetOrgainizerMeet(meets_Id['orgainzer_meetsId'])
            InvitedMeets = GetInvitationMeets(meets_Id['invitation_meetsId'])
            return jsonify({'status': "success", "code": 401, "msg": "Meeting created successfully!", "data":{"orgainizerMeets":list(OrgainizerMeets), "invitedMeets":list(InvitedMeets)}})
        return jsonify({"status": "failed", "code": 401, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error (CreateMeetRoom): Error occured during meeting room creation.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED

