import pytz


try:
    from twilio.rest import Client
    import random
    from flask import session, request, jsonify
    from dotenv import load_dotenv
    import os
    from functools import wraps
    from datetime import datetime, timedelta, date
    import uuid
    import jwt
    import boto3
    from projectModule.constants.http_status_code import HTTP_417_EXPECTATION_FAILED
    from werkzeug.utils import secure_filename
except Exception as e:
    print("Modules are Missing : {} ".format(e))

load_dotenv()

def sendOtpOnPhone(number):
    """
        This function creates and send otp to entered phone number.
        """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_TOKEN")
        client = Client(account_sid, auth_token)
        otp = generateOtp(4)
        session['SharedOTP'] = str(otp)
        message = client.messages.create(
            from_='+19704364972',
            body="Your Fornax account verification otp is " +
            str(otp) + ". It will be valid for only 5 minutes. -Fornax",
            to=number
        )
        if message.sid:
            return True
        else:
            return False
    except Exception as e:
        print("Error : Error Occured during process to send Otp on Phone.")
        print("Error is : {} ".format(e))


def generateOtp(digits):
    """
        This function generate otp based on required digits.
        """
    try:
        if digits == 4:
            return random.randrange(1000, 9999)
    except Exception as e:
        print("Error : Error generated during Otp genration.")
        print("Error is : {} ".format(e))


# def tokenReq(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         try:
#             if "Authorization" in request.headers:
#                 token = request.headers["Authorization"]
#                 print("Token is : ", token)
#                 try:
#                     jwt.decode(token, os.getenv('SECRET_KEY'))
#                 except:
#                     return jsonify({"status": "fail", "message": "unauthorized"}), 401
#                 return f(*args, **kwargs)
#             else:
#                 return jsonify({"status": "fail", "message": "unauthorized"}), 401
#         except Exception as e:
#             print("Exception is : ", e)
#     return decorated

def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms='HS256')
            print("Data is : ", data)
            # current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception as e:
            print("Exception is : ", e)
        return f(*args, **kwargs)
    return decorated


def CalculateSlots(data):
    try:
        total_video_slot = 0
        total_inClinic_slot = 0
        sd = data['dateFrom'].split('/')
        ed = data['dateTill'].split('/')
        start_date = date(year=int(sd[-1]),
                          month=int(sd[1]), day=int(sd[0]))
        end_date = date(year=int(ed[-1]), month=int(ed[1]), day=int(ed[0]))
        appoint_list = []
        mSlots = []
        aSlots = []
        eSlots = []
        curr_date = start_date
        while curr_date <= end_date:

            if data['breakType'] == "After Certain Appoinment":
                if curr_date.strftime("%A") in data['exDay']:
                    temp = 0
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": [],
                        "afternoonSlots": [],
                        "eveningSlots": [],
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    curr_date += timedelta(days=1)
                    if data['cType'] == 'Video':
                        total_video_slot += temp

                elif curr_date.strftime("%A") in data['speDay']:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0 and data[key]['isSpecific'] == True:
                                start = datetime.strptime(
                                    data[key]['sFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['sTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / data['appointTime'])):
                                    if (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))) <= end:
                                        if count == data['aAppoint']:
                                            ittr += 1
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count = 1
                                        else:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count += 1
                                        temp += 1
                                    else:
                                        break
                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []
                    
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)
                else:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0:
                                start = datetime.strptime(
                                    data[key]['nFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['nTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / data['appointTime'])):
                                    if (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))) <= end:
                                        if count == data['aAppoint']:
                                            ittr += 1
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count = 1
                                        else:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i)+(data['afterAppointBT']*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count += 1
                                        temp += 1
                                    else:
                                        break
                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []

                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)

            elif data['breakType'] == "After Every Appoinment":
                if curr_date.strftime("%A") in data['exDay']:
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": [],
                        "afternoonSlots": [],
                        "eveningSlots": [],
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    curr_date += timedelta(days=1)

                elif curr_date.strftime("%A") in data['speDay']:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0 and data[key]['isSpecific'] == True:
                                start = datetime.strptime(
                                    data[key]['sFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['sTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / (data['appointTime'] + data['everyAppointBT']))):
                                    if (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)) <= end:
                                        if key == 'mSlot':
                                            mSlots.append(
                                                {
                                                    "_id": uuid.uuid4().hex,
                                                    "time": (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)).strftime("%I:%M %p"),
                                                    "status": "A",
                                                }
                                            )
                                        elif key == 'aSlot':
                                            aSlots.append(
                                                {
                                                    "_id": uuid.uuid4().hex,
                                                    "time": (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)).strftime("%I:%M %p"),
                                                    "status": "A",
                                                }
                                            )
                                        elif key == 'eSlot':
                                            eSlots.append(
                                                {
                                                    "_id": uuid.uuid4().hex,
                                                    "time": (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)).strftime("%I:%M %p"),
                                                    "status": "A",
                                                }
                                            )
                                        temp += 1
                                    else:
                                        break
                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)

                else:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0:
                                start = datetime.strptime(
                                    data[key]['nFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['nTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / (data['appointTime'] + data['everyAppointBT']))):
                                    if (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)) <= end:
                                        if key == 'mSlot':
                                            mSlots.append(
                                                {
                                                    "_id": uuid.uuid4().hex,
                                                    "time": (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)).strftime("%I:%M %p"),
                                                    "status": "A",
                                                }
                                            )
                                        elif key == 'aSlot':
                                            aSlots.append(
                                                {
                                                    "_id": uuid.uuid4().hex,
                                                    "time": (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)).strftime("%I:%M %p"),
                                                    "status": "A",
                                                }
                                            )
                                        elif key == 'eSlot':
                                            eSlots.append(
                                                {
                                                    "_id": uuid.uuid4().hex,
                                                    "time": (start + timedelta(minutes=(data['appointTime'] + data['everyAppointBT'])*i)).strftime("%I:%M %p"),
                                                    "status": "A",
                                                }
                                            )
                                        temp += 1
                                    else:
                                        break
                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []

                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)

            elif data['breakType'] == "Both options":
                if curr_date.strftime("%A") in data['exDay']:
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": [],
                        "afternoonSlots": [],
                        "eveningSlots": [],
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    curr_date += timedelta(days=1)
                elif curr_date.strftime("%A") in data['speDay']:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0 and data[key]['isSpecific'] == True:
                                start = datetime.strptime(
                                    data[key]['sFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['sTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / (data['appointTime'] + data['everyAppointBT']))):
                                    if (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))) <= end:
                                        if count == data['aAppoint']:
                                            ittr += 1
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count = 1
                                        else:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count += 1
                                        temp =+ 1
                                    else:
                                        break

                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)
                else:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0:
                                start = datetime.strptime(
                                    data[key]['nFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['nTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / (data['appointTime']+data['everyAppointBT']))):
                                    if (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))) <= end:
                                        if count == data['aAppoint']:
                                            ittr += 1
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count = 1
                                        else:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=((data['appointTime'] + data['everyAppointBT'])*i)+((data['afterAppointBT']-data['everyAppointBT'])*ittr))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count += 1
                                        temp += 1
                                    else:
                                        break

                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)

            else:
                if curr_date.strftime("%A") in data['exDay']:
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": [],
                        "afternoonSlots": [],
                        "eveningSlots": [],
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    curr_date += timedelta(days=1)
                elif curr_date.strftime("%A") in data['speDay']:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0 and data[key]['isSpecific'] == True:
                                start = datetime.strptime(
                                    data[key]['sFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['sTill'], "%I:%M %p")

                                for i in range(int((end-start).total_seconds() / 60.0 / data['appointTime'])):
                                    if (start + timedelta(minutes=(data['appointTime']*i))) <= end:
                                        if count == data['aAppoint']:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count = 1
                                        else:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            count += 1
                                        temp += 1
                                    else:
                                        break

                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)
                else:
                    temp = 0
                    for key in data.keys():
                        if key in ["mSlot", "aSlot", "eSlot"]:
                            if len(data[key].keys()) > 0:
                                start = datetime.strptime(
                                    data[key]['nFrom'], "%I:%M %p")
                                end = datetime.strptime(
                                    data[key]['nTill'], "%I:%M %p")
                                count = 0
                                ittr = 0
                                for i in range(int((end-start).total_seconds() / 60.0 / data['appointTime'])):
                                    if (start + timedelta(minutes=(data['appointTime']*i))) <= end:
                                        if count == data['aAppoint']:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                        else:
                                            if key == 'mSlot':
                                                mSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'aSlot':
                                                aSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                            elif key == 'eSlot':
                                                eSlots.append(
                                                    {
                                                        "_id": uuid.uuid4().hex,
                                                        "time": (start + timedelta(minutes=(data['appointTime']*i))).strftime("%I:%M %p"),
                                                        "status": "A",
                                                    }
                                                )
                                        temp += 1
                                    else:
                                        break

                            else:
                                if key == 'mSlot':
                                    mSlots = []
                                elif key == 'aSlot':
                                    aSlots = []
                                elif key == 'eSlot':
                                    eSlots = []
                    appoint_list.append({
                        "_id": uuid.uuid4().hex,
                        "day": curr_date.strftime("%Y-%m-%d"),
                        "day_show": curr_date.strftime("%d %b"),
                        "type": data['cType'],
                        "morningSlots": mSlots,
                        "afternoonSlots": aSlots,
                        "eveningSlots": eSlots,
                        "created_At": datetime.now(pytz.timezone('Asia/Kolkata')),
                        "updated_At": datetime.now(pytz.timezone('Asia/Kolkata'))
                    })
                    if data['cType'] == 'Video':
                        total_video_slot += temp
                    else: 
                        total_inClinic_slot += temp
                    mSlots = []
                    aSlots = []
                    eSlots = []
                    curr_date += timedelta(days=1)

        del data, sd, ed, start_date, end_date, mSlots, aSlots, eSlots, curr_date
        return appoint_list, total_video_slot, total_inClinic_slot
    except Exception as e:
        print("Error (CalculateSlots): Error occured during calculation of slos for Doctor or Therapist.")
        print("Exception is : ", e)


EXTENSIONS_ALLOWED_IMG = ["png", "jpg", "jpeg", "gif"]
EXTENSIONS_ALLOWED_DOC = ["pdf", "txt", "odt"]
EXTENSIONS_ALLOWED_VID = ['mp4', "mpeg", "mkv"]
EXTENSIONS_ALLOWED_AUD = ["mp3", "mp4", "m4a", "aac"]
ROOT_DIR = os.path.dirname(os.path.abspath("app.py"))

def uploadFile(file, type, bucket_name):
    
    # Find type of file and setting target location.
    try:
        if type == "img":
            if file and file.filename.split(".")[-1].lower() in EXTENSIONS_ALLOWED_IMG:
                target = os.path.join(ROOT_DIR, 'client/images/')
            else:
                return "Unsupported Image."
        elif type == "doc":
            if file and file.filename.split(".")[-1].lower() in EXTENSIONS_ALLOWED_DOC:
                target = os.path.join(ROOT_DIR, 'documents/')
            else:
                return "Unsupported Document."
        elif type == "vid":
            if file and file.filename.split(".")[-1].lower() in EXTENSIONS_ALLOWED_VID:
                target = os.path.join(ROOT_DIR, 'videos/')
            else:
                return "Unsupported Video."
        elif type == "aud":
            if file and file.filename.split(".")[-1].lower() in EXTENSIONS_ALLOWED_AUD:
                target = os.path.join(ROOT_DIR, 'audios/')
            else:
                return "Unsupported Audio."
        else:
            return "File type not supported."
    except Exception as e:
        print(
            "Error : Error occured while distinguishing file type and setting target location.")
        print("Error is : ", str(e))

    # Saving file on static location ops.
    try:
        if not os.path.isdir(target):
                os.mkdir(target)

        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
    except Exception as e:
        print(
            "Error : Error occured while saving file on static location.")
        print("Error is : ", str(e))

    # Uploading on s3 ops.
    try:
        s3 = boto3.client('s3')
        s3 = boto3.resource(
            service_name='s3',
            region_name=os.getenv("S3_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_ACCESS_SECRET")
            )
        s3.meta.client.upload_file(destination, bucket_name, filename)
    except Exception as e:
        print(
            "Error : Error occured while uploading file on s3 operation.")
        print("Error is : ", str(e))

    # Deleting saved file from server ops.
    try:
        os.unlink(os.path.join(target, filename))
    except Exception as e:
        print(
            "Error : Error occured while deleting saved file from server.")
        print("Error is : ", str(e))


    return "https://{}.s3.{}.amazonaws.com/{}".format(bucket_name, os.getenv("S3_REGION"), filename)


    return 'Image Upload Successfully'