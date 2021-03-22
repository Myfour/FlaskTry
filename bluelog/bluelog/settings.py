import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 5
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15
    # 发邮件相关
    BLUELOG_ADMIN_EMAIL = '913906842@qq.com'
    # SERVER_NAME = '127.0.0.1:5000' # 当url_for中使用了参数_external时需要设置SERVER_NAME配置,但是好像也不是这样
    BLUELOG_THEMES = {
        'perfect_blue': 'Perfect Blue',
        'black_swan': 'Black Swan',
        'minty': 'Minty'
    }


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"data-dev.db")}'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}