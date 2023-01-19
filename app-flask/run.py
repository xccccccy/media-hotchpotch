import sys

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from config.config import register_logging
from route.main_route import init_route
from database.dbop import init_database
from mail.mail import init_mail

app = Flask(
    'MEDIA-HOTCHPOTCH',
    template_folder='./static',  # templates 路径 路由中 render_template 所直接访问相对地址
    static_folder='./static',  #  静态资源路径
    static_url_path='/static' #  访问静态资源前缀
)

app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'

CORS(app, supports_credentials=True)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

register_logging(app)
init_database(app)
init_route(app)
init_mail(app)


    
if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1:
        debug = True
    # app.run(debug=debug, host='0.0.0.0', port=5001)
    app.run(debug=True, host='0.0.0.0', port=5001)
