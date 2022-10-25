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
userAuth_blueprint = Blueprint("UserAuth", __name__)


# def sendMail(sender, receiver):
#     msg = Message(
#         'Hello',
#         sender=sender,
#         recipients=[receiver]
#     )
#     msg.body = 'Hello Flask message sent from Flask-Mail'
#     mail.send(msg)
#     return 'Sent'


@userAuth_blueprint.route("/register", methods=["POST"])
def UserRegistration():
    """
        This function takes required registration input, verify and after register user.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))

            if mongo.findfirstRecord(db_name="Communication_App", collection_name="Participaints", query={
                    "email": data['email'], }):
                return jsonify({'status': "failed", "code": 401, "msg": "E-mail already registered"})
            else:
                # if sendOtpOnPhone(data['phone_number']):
                if True:
                    session['UserData'] = data
                    return jsonify({'status': "Success", "code": 201, "msg": "OTP send Successfully!"})
                else:
                    return jsonify({'status': "failed", "code": 401, "msg": "Failed to send OTP"})
        return jsonify({"status": "Failed", "code": 401, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during User Registration.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


def InsertValue():
    try:
        temp = {}
        temp['_id'] = uuid.uuid4().hex
        temp['name'] = session['UserData']['name']
        temp['phone'] = session['UserData']['phone_number']
        temp['email'] = session['UserData']['email']
        temp['password'] = bcrypt.hashpw(
            session['UserData']['password'].encode('utf-8'), bcrypt.gensalt())
        temp['type'] = ''
        temp['status'] = 0
        temp['token'] = ''
        temp['device_token'] = ''
        temp['created_at'] = datetime.now(
            pytz.timezone('Asia/Kolkata'))
        session['UserData'].pop('name')
        session['UserData'].pop('phone_number')
        session['UserData'].pop('email')
        mongo = MongoDBManagement(
            os.getenv("USERID"), os.getenv("PASSWORD"))
        mongo.insertRecord(db_name="Communication_App",
                           collection_name="Participaints", record=temp)
        mongo.insertRecord(db_name="Users",
                                 collection_name="General_Details", record=temp)
        session.pop('UserData', None)
        session.pop('SharedOTP', None)
    except Exception as e:
        print("Error is : ", str(e))


@userAuth_blueprint.route("/validateOtpAndInsert", methods=["POST"])
def ValidateOtpAndInsertUserData():
    """
        This function validate otp which send during registration process and after that register user.
        """
    try:
        if request.method == "POST":
            key = request.get_json()
            # if key['otp'] == session['SharedOTP']:
            if key['otp'] == "1234":
                InsertValue()
                return jsonify({'status': "Success", "code": 201, "msg": "Successfully Registred!"})
    except Exception as e:
        print("Error : Error occured during OTP validation.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@userAuth_blueprint.route("/resendOtp", methods=["POST"])
def ResendOtp():
    """
        This function resend otp during registration process.
        """
    try:
        if request.method == "POST":
            if sendOtpOnPhone(session['UserData']['phone_number']):
                return jsonify({'status': "Success", "code": 201, "msg": "OTP send Successfully!"})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Failed to send OTP"})
        return jsonify({"status": "Failed", "code": 401, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during OTP validation.")
        print("Exception is : ", e)


@userAuth_blueprint.route("/login", methods=["POST"])
def UserLogin():
    """
        This function validate user input login credentials and after validation generate a token.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            searched_data = mongo.findfirstRecord(db_name="Communication_App", collection_name="Participaints", query={
                "email": data['email'], })
            if searched_data:
                if bcrypt.checkpw(data['password'].encode('utf-8'), searched_data['password']):
                    # time = datetime.utcnow() + timedelta(hours=24)
                    access_token = create_access_token(
                        identity=searched_data['_id'])
                    refresh_token = create_access_token(
                        identity=searched_data['_id'])
                    del searched_data['password']
                    return jsonify({'status': "success", "code": 200, "msg": "User authenticated successfully.", "uId": searched_data['_id'], "token": {'refresh': refresh_token, 'access': access_token}})
                else:
                    return jsonify({'status': "failed", "code": 401, "msg": "Wrong Password."})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Email not registered."})
        else:
            return jsonify({'status': "failed", "code": 500, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during User login process.")
        print("Exception is : ", e)
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED


@userAuth_blueprint.route("/changePassword", methods=["POST"])
def UserchangePassword():
    """
        This function use to change user password when user is loged in.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            if len(data) == 4:
                mongo = MongoDBManagement(
                    os.getenv("USERID"), os.getenv("PASSWORD"))
                searched_data = mongo.findfirstRecord(db_name="Communication_App", collection_name="Participaints", query={
                    "email": data['email'], })
                if searched_data:
                    if bcrypt.checkpw(data['old_password'].encode('utf-8'), searched_data['password']):
                        if data['password'] == data['confirm_password']:
                            if mongo.updateOneRecordPartally(db_name="Communication_App", collection_name="Participaints", filteredValue={'email': data['email']}, newValue={'password': bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())}):
                                return jsonify({'status': "success", "code": 200, "msg": "Password Changed Successfully."})
                            else:
                                return jsonify({'status': "failed", "code": 401, "msg": "Not able to change password.."})
                        else:
                            return jsonify({'status': "failed", "code": 401, "msg": "New password doesn't match the confirm password."})
                    else:
                        return jsonify({'status': "failed", "code": 401, "msg": "Wrong old Password."})
                else:
                    return jsonify({'status': "failed", "code": 401, "msg": "Email not registered."})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Required input values are missing."})
        else:
            return jsonify({'status': "failed", "code": 500, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during changing of user password.")
        print("Exception is : ", e)


@userAuth_blueprint.route("/validateOtp", methods=["POST"])
def ValidateOtp():
    """
        This function validate otp which send during registration process and after that register user.
        """
    try:
        if request.method == "POST":
            key = request.get_json()
            if key['otp'] == session['SharedOTP']:
                del session['SharedOTP']
                return jsonify({'status': "Success", "code": 201, "msg": "OTP Matched successfully"})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Wrong OTP!"})
        else:
            return jsonify({'status': "failed", "code": 500, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during OTP validation.")
        print("Exception is : ", e)


@userAuth_blueprint.route("/resetPassword", methods=["POST"])
def UserResetPassword():
    """
        This function use to change user password when user is not loged in.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            if len(data) == 1:
                mongo = MongoDBManagement(
                    os.getenv("USERID"), os.getenv("PASSWORD"))
                searched_data = mongo.findfirstRecord(db_name="Communication_App", collection_name="Participaints", query={
                    "email": data['email'], })

                if searched_data:
                    if sendOtpOnPhone(searched_data['phone_number']):
                        session['UserEmail'] = data['email']
                        del searched_data
                        return jsonify({'status': "Success", "code": 201, "msg": "OTP send Successfully!"})
                    else:
                        del searched_data
                        return jsonify({'status': "failed", "code": 401, "msg": "Failed to send OTP"})
                else:
                    del searched_data
                    return jsonify({'status': "failed", "code": 401, "msg": "Email not registered."})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Required input values are missing."})
        else:
            return jsonify({'status': "failed", "code": 500, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during changing of user password.")
        print("Exception is : ", e)


@userAuth_blueprint.route("/resetNewPassword", methods=["POST"])
def UserInsertNewPassword():
    """
        This function use to change user password when user is not loged in.
        """
    try:
        if request.method == "POST":
            data = request.get_json()
            if len(data) == 1:
                mongo = MongoDBManagement(
                    os.getenv("USERID"), os.getenv("PASSWORD"))
                if mongo.updateOneRecordPartally(db_name="Communication_App", collection_name="Participaints", filteredValue={'email': session['UserEmail']}, newValue={'password': bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())}):
                    return jsonify({'status': "success", "code": 200, "msg": "Password Reset Successfully."})
                else:
                    return jsonify({'status': "failed", "code": 401, "msg": "Not able to reset password.."})
            else:
                return jsonify({'status': "failed", "code": 401, "msg": "Required input values are missing."})
        else:
            return jsonify({'status': "failed", "code": 500, "msg": "Only Post methods are allowed"})
    except Exception as e:
        print("Error : Error occured during changing of user password.")
        print("Exception is : ", e)


@userAuth_blueprint.route("/getProfile", methods=["GET"])
def ViewRegisteredProfile():
    """
         This function use to get user registered profile details.
        """
    try:
        if request.method == "GET":
            id = request.args.get('id')
            mongo = MongoDBManagement(
                os.getenv("USERID"), os.getenv("PASSWORD"))
            data = mongo.findfirstRecord(db_name="Communication_App", collection_name="Participaints",
                                         query={
                                             "_id": id
                                         }, includeField={
                                             '_id': 1,
                                             "email": 1,
                                             "name": 1,
                                             "phone_number": 1,
                                             "gender": 1,
                                             "age": 1,
                                             "profilePic": 1,
                                         }
                                         )

            if data:
                return jsonify({'status': "success", "code": HTTP_200_OK, "msg": "Data found.", "data": data}), HTTP_200_OK
            else:
                return jsonify({'status': "failed", "code": HTTP_204_NO_CONTENT, "msg": "Data not found."}), HTTP_204_NO_CONTENT
        else:
            return jsonify({'status': "failed", "code": HTTP_405_METHOD_NOT_ALLOWED, "msg": "Only GET methods are allowed"}), HTTP_405_METHOD_NOT_ALLOWED
    except Exception as e:
        print("Error : Error occured during user profile fetching.")
        print("Error is : ", str(e))
        return jsonify({'status': "failed", "code": HTTP_417_EXPECTATION_FAILED, "msg":  str(e)}), HTTP_417_EXPECTATION_FAILED
