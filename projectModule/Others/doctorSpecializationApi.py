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
doctorSpecializationApi_blueprint = Blueprint(
    "DoctorSpecializationApi", __name__)


@doctorSpecializationApi_blueprint.route("/insert", methods=["POST"])
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
                                   collection_name="Doctor_Specialities", record=data)
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


@doctorSpecializationApi_blueprint.route("/getAll", methods=["GET"])
def GetAllSpecializations():
    """
         This function use to get all docter specilization.
        """
    try:
        if request.method == "GET":
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.findAllRecords(
                db_name="Others", collection_name="Doctor_Specialities", includeField={
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
        print("Error : Error occured during doctor specialization fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@doctorSpecializationApi_blueprint.route('/getServices', methods=["POST"])
def GetServicesById():
    """
         This function use to get services by particular specialization id.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            docServices = mongo.findfirstRecord(
                db_name="Others", collection_name="Doctor_Specialities", query={
                    "_id": data['id']
                }, includeField={
                    "_id": 1,
                    "services": 1,
                    "title": 1
                })

            if docServices:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": docServices}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during doctor specialization fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@doctorSpecializationApi_blueprint.route('/getAoS', methods=["POST"])
def GetAreasOfSpecializationById():
    """
         This function use to get Areas Of Specialization by particular specialization id.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            docAos = mongo.findfirstRecord(
                db_name="Others", collection_name="Doctor_Specialities", query={
                    "_id": data['id']
                }, includeField={
                    "_id": 1,
                    "aos": 1,
                    "title": 1
                })

            if docAos:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": docAos}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during doctor specialization fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@doctorSpecializationApi_blueprint.route("/getLimitedSpe", methods=["GET"])
def GetLimitedSpecializations():
    """
         This function use to get Limited number of doctor specilization.
        """
    try:
        if request.method == "GET":
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.findLimitedRecords(
                db_name="Others", collection_name="Doctor_Specialities", limit=4, includeField={
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
        print("Error : Error occured during limited doctor specialization fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED
