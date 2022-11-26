try:
    from flask import Blueprint, jsonify, request
    from projectModule.dbOperations.mongoOP import MongoDBManagement
    from dotenv import load_dotenv
    from datetime import datetime
    import os
    import uuid
    import pytz
    from projectModule.CommonOperations.twilioOperation import CreateVideoRoom
    from projectModule.authentications.userAuthApi import GetMeetsId
    from projectModule.CommonOperations.twilioOperation import CreateAccessToken_Video
    from projectModule.constants.http_status_code import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_417_EXPECTATION_FAILED
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

            # video_room_sid = CreateVideoRoom(data['m_title'])
            video_room_sid = os.getenv('VIDEO_ROOM_SID')

            m_id = InsertInVR(data, video_room_sid)
            temp = []
            for item in data['invities']:
                temp.append(item['id'])
            if InsertInUserCollection(m_id, temp, data['created_by']['id']) == True:
                return jsonify({'status': "success", "code": 200, "msg": "Meeting created successfully!"}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Failed to create meeting link."}), HTTP_401_UNAUTHORIZED
        return jsonify({"status": "failed", "code": 401, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error (CreateMeetRoom): Error occured during meeting room creation.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


def InsertInVR(data, video_room_sid):
    try:
        temp = {}
        id = uuid.uuid4().hex
        temp['_id'] = id
        temp['video_room_sid']=video_room_sid
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
        print("Error is : ", str(e))


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
            return jsonify({'status': "success", "code": 401, "msg": "Meeting created successfully!", "data":{"orgainizerMeets":list(OrgainizerMeets), "invitedMeets":list(InvitedMeets)}}), HTTP_200_OK
        return jsonify({"status": "failed", "code": 401, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error (CreateMeetRoom): Error occured during meeting room creation.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED

@videoRooms_blueprint.route("/enterR", methods=["GET"])
def CreateMeetRoomAccessToken():
    """
        """
    try:
        if request.method == "GET":
            roomName = request.args.get('id')
            room_Access_Token = CreateAccessToken_Video(roomName)
            return jsonify({'status': "success", "code": 401, "msg": "Access token created successfully!", "token":room_Access_Token}), HTTP_200_OK
        return jsonify({"status": "failed", "code": 401, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error (CreateMeetRoomAccessToken): Error occured during meeting room Access token creation.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED