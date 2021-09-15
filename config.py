import os, binascii


class Config(object):
    # path of the folder where the file is to be uploaded to the server
    UPLOAD_FOLDER = '/Users/mmestre/PycharmProjects/flaskProject/Sandbox/upload'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 Megabytes
    SECRET_KEY = binascii.hexlify(os.urandom(24))
