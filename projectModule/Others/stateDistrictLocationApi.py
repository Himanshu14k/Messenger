from projectModule.constants.http_status_code import HTTP_204_NO_CONTENT, HTTP_302_FOUND, HTTP_417_EXPECTATION_FAILED


try:
    from flask import Blueprint, jsonify, request, session
    from projectModule.dbOperations.mongoOP import MongoDBManagement
    from dotenv import load_dotenv
    import bcrypt
    from datetime import datetime, timedelta
    import os
    import uuid
    import pytz
    from projectModule.constants.http_status_code import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE
except Exception as e:
    print("Modules are Missing : {} ".format(e))


load_dotenv()
stateDistrictLocation_blueprint = Blueprint(
    "StateDistrictLocation", __name__)


@stateDistrictLocation_blueprint.route("/getStates", methods=["POST"])
def GetAllStates():
    """
         This function use to get all State Districts And Areas.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.findAllRecords(
                db_name="Others", collection_name="State_District_Areas",

                includeField={
                    "_id": 1,
                    "title": 1,
                }))

            if dataList:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": dataList}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND
        else:

            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during state, district and area data fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@stateDistrictLocation_blueprint.route("/getDistricts", methods=["POST"])
def GetAllDistrictsByStateID():
    """
         This function use to get all State Districts And Areas.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = mongo.findfirstRecord(
                db_name="Others", collection_name="State_District_Areas",
                query={"_id": data["id"]
                       },
                includeField={
                    "_id": 1,
                    "districts": 1
                })

            if dataList:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": dataList}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND
        else:

            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during state, district and area data fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@stateDistrictLocation_blueprint.route("/getAreas", methods=["POST"])
def GetAllAreasByStateAndDistrictID():
    """
         This function use to get all State Districts And Areas.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            dataList = list(mongo.aggregateRecord(db_name="Others", collection_name="State_District_Areas",
                                                  aggeregationQuery=[
                                                      {"$match": {
                                                          "_id": data['sId'],
                                                          "districts._id":data['dId'],
                                                      }
                                                      },
                                                      {"$project": {
                                                          "districts": {"$filter": {
                                                              "input": "$districts",
                                                              "as": "districts",
                                                              "cond": {
                                                                  "$eq": [
                                                                      "$$districts._id",
                                                                      data['dId']
                                                                  ]
                                                              }
                                                          }
                                                          },

                                                      }
                                                      },
                                                      {"$unwind": "$districts"
                                                       },
                                                      {
                                                          "$replaceRoot": {
                                                              "newRoot": "$districts"
                                                          }
                                                      }
                                                  ]
                                                  ))

            if dataList:
                return jsonify({'status': "Success", "code": HTTP_200_OK, "data": dataList[0]}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_404_NOT_FOUND, "msg": "Records not found."}), HTTP_404_NOT_FOUND

        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only Post methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during state, district and area data fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED
