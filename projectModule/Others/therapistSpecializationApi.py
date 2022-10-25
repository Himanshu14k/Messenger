try:
    from flask import Blueprint, jsonify, request
    from projectModule.dbOperations.mongoOP import MongoDBManagement
    from dotenv import load_dotenv
    from datetime import datetime
    import os
    import uuid
    import pytz
    from projectModule.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE, HTTP_417_EXPECTATION_FAILED
except Exception as e:
    print("Modules are Missing : {} ".format(e))


load_dotenv()
therapistSpecializationApi_blueprint = Blueprint(
    "TherapistSpecializationApi", __name__)


@therapistSpecializationApi_blueprint.route("/insert", methods=["POST"])
def InsertSpecialization_Doc():
    try:
        if request.method == "POST":
            data = request.get_json()
            if len(data) == 4:
                mongo = MongoDBManagement(
                    os.getenv("USERID"), os.getenv("PASSWORD"))
                data['_id'] = uuid.uuid4().hex
                for key in data.keys():
                    if key in ["services", "areasOfSpecialization"]:
                        for i in data[key]:
                            i.update({"_id": uuid.uuid4().hex})
                data['createdAt'] = datetime.now(pytz.timezone('Asia/Kolkata'))
                data['updatedAt'] = datetime.now(pytz.timezone('Asia/Kolkata'))
                mongo.insertRecord(db_name="Others",
                                   collection_name="Therapist_Specialities", record=data)
                del data
                return jsonify({'status': "success", "msg": "Specilization Inserted Successfully."}), HTTP_201_CREATED
            else:
                del data
                return jsonify({'status': "failed", "msg": "Required input values are missing."}), HTTP_406_NOT_ACCEPTABLE
        else:
            return jsonify({'status': "failed", "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED

    except Exception as e:
        print("Error (InsertSpecialization_Doc): Error occured during insertion of doctor specilization.")
        print("Exception is : ", e)


@therapistSpecializationApi_blueprint.route("/getAOS", methods=["GET"])
def GetAllSpecializations():
    """
         This function use to get all therapist specialization.
        """
    try:
        if request.method == "GET":
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.findAllRecords(
                db_name="Others", collection_name="Therapist_Specialities", includeField={
                    "_id": 1,
                    "title": 1,
                    "image": 1
                }))

            if dataList:
                return jsonify({'status': "Success", "code": 200, "data": dataList}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": 201, "msg": "Records not found."}), HTTP_200_OK
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only GET methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during Therapist specialization fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@therapistSpecializationApi_blueprint.route('/getSer', methods=["GET"])
def GetServicesById():
    """
         This function use to get services .
        """
    try:
        if request.method == "GET":
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            therapistServices = list(mongo.findAllRecords(
                db_name="Others", collection_name="Therapist_Services", includeField={
                    "_id": 1,
                    "title": 1
                }))

            if therapistServices:
                return jsonify({'status': "Success", "code": 200, "data": therapistServices}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": 203, "msg": "Records not found."}), HTTP_200_OK
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only GET methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during Therapist service data fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED
