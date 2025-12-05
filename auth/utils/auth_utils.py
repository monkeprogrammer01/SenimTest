from bcrypt import gensalt, hashpw, checkpw

def get_password_hash(password):
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    try:
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False

