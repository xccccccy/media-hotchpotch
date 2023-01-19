from flask_mail import Mail, Message
import random

app = None
mail = None

def init_mail(_app):
    global app, mail
    app = _app
    app.config["MAIL_SERVER"] = "smtp.163.com"
    app.config["MAIL_PORT"] = 465  # 设置邮箱端口为465
    app.config["MAIL_USE_SSL"] = True  # QQ邮箱需要开启SSL
    app.config["MAIL_USERNAME"] = "xcy_0820@163.com"
    app.config["MAIL_PASSWORD"] = "SFHAQQIKCMEJTCKO"    #授权码
    mail = Mail(app)

# 注意： 这里我们生成的是0-9A-Za-z的列表，当然你也可以指定这个list，这里很灵活
# 比如： code_list = ['P','y','t','h','o','n','T','a','b'] # PythonTab的字母
code_list = []
for i in range(10): # 0-9数字
    code_list.append(str(i))
for i in range(65, 91): # 对应从“A”到“Z”的ASCII码
    code_list.append(chr(i))
for i in range(97, 123): #对应从“a”到“z”的ASCII码
    code_list.append(chr(i))

def generate_verification_code(len=6):
    ''' 随机生成6位的验证码 '''
    myslice = random.sample(code_list, len) # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice) # list to string
    return verification_code


def send_message(_recipient="710813206@qq.com", _message="hello"):
    """
    Message发送邮件信息， sender为发送者邮箱， recipients为接受者邮箱
    """
    message = Message("< xcya.cn > 验证码", sender=app.config["MAIL_USERNAME"], recipients=[_recipient])
    message.body = _message

    # 添加附件
    # with app.open_resource("E:\python\Demo.doc") as doc:
    #     # attach("文件名", "类型", 读取文件）
    #     message.attach("Demo.doc", 'application/octet-stream', doc.read())
    with app.app_context():
        mail.send(message)
    return "发送成功"
