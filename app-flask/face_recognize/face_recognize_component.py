import cv2
import face_recognition
import os
import numpy as np
import base64

white_map = {}

# 读取本地肖像编码库，建立识别白名单, 初始化
def load_portrait():
    '''
    path: 肖像库路径
    '''
    # 消息提示
    print('>>>本地图像库读取中，请稍后')
    # 建立白名单
    white_map = {}
    for face_id in os.listdir('./face_recognize/face_encodings'):
        if face_id.split('.')[1] != "npy":
            continue
        face_id = face_id.split('.')[0]
        avg_coding = np.load('./face_recognize/face_encodings/' + face_id + '.npy')
        white_map[face_id] = avg_coding
    print(white_map.keys())
    print('>> over.')
    return white_map

# 初始化
white_map = load_portrait()

# 根据白名单，提取肖像编码
known_face_encodings = list(white_map.values())
known_face_names = np.array(list(white_map.keys()))

def recognize(img_base64):
    global known_face_encodings, known_face_names
    face_encoding = img_base64_to_face_encoding(img_base64)
    if face_encoding.any():
        # 匹配
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.38)
        if True in matches:
            return True, known_face_names[matches][0]
        else:
            return True, None
    else:
        return False, None

def add_face_recognize(img_base64s, face_id):
    global known_face_encodings, known_face_names, white_map
    face_encodings = []
    for img_base64 in img_base64s:
        face_encoding = img_base64_to_face_encoding(img_base64.split(',')[1])
        if face_encoding.any():
            face_encodings.append(face_encoding)
        else:
            return False
    for i in range(1, 3):
        if add_face_encoding_compare(face_encodings[i], face_encodings[0]):
            continue
        else:
            return False
    face_encodings = np.asarray(face_encodings)
    avg_face_encoding = np.mean(face_encodings, axis=0)
    white_map[face_id] = avg_face_encoding
    known_face_encodings = list(white_map.values())
    known_face_names = np.array(list(white_map.keys()))
    print(white_map.keys())
    np.save('./face_recognize/face_encodings/' + face_id + '.npy', avg_face_encoding)
    return True

def img_base64_to_face_encoding(img_base64): # img base64格式转face encoding， 只取第一个人脸编码
    frame = base64_to_img(img_base64)
    if frame.shape[1] > 150:
        zoom = frame.shape[1] / 150
    else:
        zoom = 1
    # 图像预处理（包括大小调整、格式转换）
    frame = cv2.resize(frame, (0, 0), fx=1 / zoom, fy=1 / zoom) # 调整图像大小，以减小计算需求
    # frame = frame[:, :, ::-1] # BGR->RGB

    # 计算人脸的编码值
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    if len(face_encodings) > 0:
        return face_encodings[0]
    else:
        return np.array([0])

def add_face_encoding_compare(now_face_encoding, face_encoding):
    return face_recognition.compare_faces([now_face_encoding], face_encoding, 0.38)[0]

def base64_to_img(base64_str):
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)#将base64转换为二进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")# 二进制转换为一维数组
    img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)# 用cv2解码为三通道矩阵
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)# BGR2RGB
    return img_array

def img_to_base64(img_array):
    # 传入图片为RGB格式numpy矩阵，传出的base64也是通过RGB的编码
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR) #RGB2BGR，用于cv2编码
    encode_image = cv2.imencode(".jpg", img_array)[1] #用cv2压缩/编码，转为一维数组
    byte_data = encode_image.tobytes() #转换为二进制
    base64_str = base64.b64encode(byte_data).decode("ascii") #转换为base64
    return base64_str