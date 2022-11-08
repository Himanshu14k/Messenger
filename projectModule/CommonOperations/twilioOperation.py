# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def CreateVideoRoom(roomName):
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_TOKEN")
        client = Client(account_sid, auth_token)

        room = client.video.v1.rooms.create(unique_name=roomName)

        print(room.sid)
        print(room)
    except Exception as e:
        print("Error is : ", str(e))


def CreateAccessToken_Video(roomName):
    try:
        # Required for all Twilio Access Tokens
        # To set up environmental variables, see http://twil.io/secure
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        api_key = os.getenv('TWILIO_API_KEY')
        api_secret = os.getenv('TWILIO_API_KEY_SECRET')

        # required for Video grant
        identity = 'user'

        # Create Access Token with credentials
        token = AccessToken(account_sid, api_key, api_secret, identity=identity)

        # Create a Video grant and add to token
        video_grant = VideoGrant(room=roomName)
        token.add_grant(video_grant)

        # Return token info as JSON
        print(token.to_jwt())

    except Exception as e:
        print("Error is : ", str(e))
