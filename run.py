
try:
    from flask import jsonify
    from projectModule import socketio, app
    from waitress import serve
except Exception as e:
    print("Modules are Missing : {} ".format(e))

if __name__ == '__main__':
    try:
        # serve(socketio.run(app, debug=True))
        socketio.run(app, debug=True, port=5006)
    except Exception as e:
        print("Error : Error ouccured in root file.")
        print("Exception is : ", str(e))
