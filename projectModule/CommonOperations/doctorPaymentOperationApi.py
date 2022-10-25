try:
    from flask import Blueprint, jsonify, request, session
    from projectModule.dbOperations.mongoOP import MongoDBManagement
    from dotenv import load_dotenv
    import bcrypt
    from datetime import datetime, timedelta
    from projectModule.commonOperations import sendOtpOnPhone
    import os
    from bson import ObjectId
    import uuid
    import pytz
    from projectModule.constants.http_status_code import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_302_FOUND, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE
except Exception as e:
    print("Modules are Missing : {} ".format(e))


load_dotenv()
doctorPaymentOperation_blueprint = Blueprint(
    "DoctorPaymentOperation", __name__)

# Insert OPERATIONS


@doctorPaymentOperation_blueprint.route("/insertOne", methods=["POST"])
def InsertPaymentData_Doc():
    """
        This function use to insert many appoinment slot of doctor in their collection "AppointmentSlots_Doctor"
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            if len(data) == 2:
                data['appointments']['_id'] = uuid.uuid4().hex
                for j in range(len(data['appointments']['issues'])):
                    data['appointments']['issues'][j].update(
                        {"_id": uuid.uuid4().hex})
                mongo.insertInEmbeddedRecord(db_name="FornaxDB", collection_name="Payments_Doctor", filter={
                    "authID": data["authID"]}, subField="payments", record=data['payments'])
                mongo.updateOneRecordPartally(db_name="FornaxDB", collection_name="Payments_Doctor", filteredValue={
                    'authID': data['authID']}, newValue={"updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))}, upsert=True)
                del data
                return jsonify({'status': "success", "code": 200, "msg": "Registered successfully."})
            else:
                del data
                return jsonify({'status': "failed", "code": 401, "msg": "Required input values are missing."})
        else:
            del data
            return jsonify({'status': "failed", "code": 500, "msg": "Only Post methods are allowed"})

    except Exception as e:
        print("Error (BookAppoinmentSlotD): Error occured during insertion of doctor appoinment.")
        print("Exception is : ", e)
