import os

class Config(object):
    SECRET_KEY = os.urandom(11)
    # SERVER_NAME = "mensagemdecoded.pt"

class ProductionConfig(Config):
    DEBUG = False
    
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True