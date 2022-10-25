try:
    from flask import Blueprint, jsonify, request, session
    from projectModule.dbOperations.mongoOP import MongoDBManagement
    from dotenv import load_dotenv
    import bcrypt
    from datetime import datetime, timedelta
    import os
    import uuid
    import pytz
    from projectModule.constants.http_status_code import HTTP_201_CREATED, HTTP_417_EXPECTATION_FAILED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE
except Exception as e:
    print("Modules are Missing : {} ".format(e))


load_dotenv()
diffCaringSpRolesApi_blueprint = Blueprint(
    "DiffCaringSpRolesApi", __name__)


@diffCaringSpRolesApi_blueprint.route("/insert", methods=["POST"])
def InsertRoles_DiffCaringSP():
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            data['_id'] = uuid.uuid4().hex
            data['createdAt'] = datetime.now(pytz.timezone('Asia/Kolkata'))
            data['updatedAt'] = datetime.now(pytz.timezone('Asia/Kolkata'))
            mongo.insertRecord(db_name="Others",
                               collection_name="DiffCaringSP_Roles", record=data)
            del data
            return jsonify({'status': "success", "msg": "Roles Inserted Successfully."}), HTTP_201_CREATED
        else:
            return jsonify({'status': "failed", "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED

    except Exception as e:
        print("Error (InsertRoles_DiffCaringSP): Error occured during insertion of DiffCaringSP roles.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@diffCaringSpRolesApi_blueprint.route("/getAllTitle", methods=["GET"])
def GetAllRolesTitle():
    """
         This function use to get all diffcaringSP roles title.
        """
    try:
        if request.method == "GET":
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.findAllRecords(
                db_name="Others", collection_name="DiiffCaringSP_Roles", includeField={
                    "_id": 1,
                    "title": 1,
                }))

            if dataList:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": dataList}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only GET methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error (GetAllRolesTitle): Error occured during diffcaringSp roles fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@diffCaringSpRolesApi_blueprint.route("/getAll", methods=["GET"])
def GetAllRoles():
    """
         This function use to get all diffcaringSP roles.
        """
    try:
        if request.method == "GET":
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.findAllRecords(
                db_name="Others", collection_name="DiiffCaringSP_Roles", includeField={
                    "_id": 1,
                    "title": 1,
                    "image": 1
                }))

            if dataList:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": dataList}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only GET methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error (GetAllRoles): Error occured during diffcaringSp roles fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED
