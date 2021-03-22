from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
debugtoolbar = DebugToolbarExtension()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate(db=db)


# 好像是决定了current_user返回的对象是什么
@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


# 设置了login_required的view需要跳转到这个view中
login_manager.login_view = 'auth.login'
# 认证不成功时自动flash的提示类型
login_manager.login_message_category = 'warning'
login_manager.login_message = '请先登录'

# 实现全局的csrf保护
