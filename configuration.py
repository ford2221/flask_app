class BaseConfig(object):
    'Base configuracion'
    USER_APP_NAME = 'FlaskPractice'
    SECRET_KEY = 'b6026f861fd41a94c3389d54293de9d04bde6f7c'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/udemydb'
    RECAPTCHA_PUBLIC_KEY = '6LfDdE8aAAAAAP9PWtxDJLGuDLxr-lRnrSYVlN_p'
    RECAPTCHA_PRIVATE_KEY = '6LfDdE8aAAAAADWyu3Il81pyalHcha-MedIjBwHy'
    BABEL_TRANSLATION_DIRECTORIES = '/home/linuxhack/Descargas/udemy/flask_app/translations'
    USER_ENABLE_EMAIL = True
   # WTF_CSRF_TIME_LIMIT = 10
class ProductionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'b6026f861fd41a94c3389d54293de9d04bde6f7c'
    MAIL_SUPPRESS_SEND = False
    MAIL_SERVER = "smtp.mailtrap.io"
    MAIL_PORT = 2525
    MAIL_USERNAME = "9473d06e5bf51e"
    MAIL_PASSWORD = "2c4a659450a229"
   # MAIL_DEFAULT_SENDER = ('ford of udemy', 'ford321@gmail.com')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    USER_EMAIL_SENDER_EMAIL = 'ford321@gmail.com'
    CACHE_TYPE = 'simple'