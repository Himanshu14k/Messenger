try:
    from projectModule import app
    from flask_bcrypt import Bcrypt
except Exception as e:
    print("Modules are Missing : {} ".format(e))

bcrypt = Bcrypt(app)


def passHash(pass):
    return bcrypt.generate_password_hash(pass).decode('utf-8')
