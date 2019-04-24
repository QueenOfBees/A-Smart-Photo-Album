from gevent import monkey;

monkey.patch_socket()
import os
import threading
import time
from urllib.request import urlretrieve

from PIL import Image
from imageai.Detection import ObjectDetection
from imageai.Prediction import ImagePrediction
import numpy as np
import json
import logging, gevent

"""
    :param url:str
    :return res:json
"""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# IMAGE_URL = sys.argv[1][1: -1].replace("\"", "").split(',')
# default url
IMAGE_URL = []

abs_path = "C:/Users/Firefox/PycharmProjects/D/src/"
abs_image_path = r"C:\Users\Firefox\PycharmProjects\D\images"
d = ObjectDetection()
d.setModelTypeAsYOLOv3()
d.setModelPath("C:/Users/Firefox/PycharmProjects/D/models/yolov3.h5")
prediction = ImagePrediction()
prediction.setModelTypeAsSqueezeNet()
prediction.setModelPath(r"C:\Users\Firefox\PycharmProjects\D\models\squzee.h5")
actual_labels = ["person", "bicycle", "car", "motorcycle", "airplane",
                 "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
                 "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear",
                 "zebra",
                 "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
                 "snowboard",
                 "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                 "tennis racket",
                 "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich",
                 "orange",
                 "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant",
                 "bed",
                 "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
                 "microwave",
                 "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
                 "hair dryer",
                 "toothbrush"]
actual_labels_cn = ["人", "自行车", "汽车", "摩托车", "飞机",
                    "公共汽车", "火车", "卡车", "船", "交通信号灯", "消防栓", "停车标识",
                    "停车计时器", "长椅", "鸟", "猫", "狗", "马", "羊", "奶牛", "大象", "熊",
                    "斑马",
                    "长颈鹿", "背包", "雨伞", "手提包", "领带", "手提箱", "飞盘", "雪橇",
                    "滑雪板",
                    "运动球", "风筝", "棒球棍", "棒球手套", "滑板", "冲浪板",
                    "网球拍",
                    "瓶子", "酒杯", "杯子", "叉子", "刀", "勺子", "碗", "香蕉", "苹果", "三明治",
                    "橘子",
                    "西兰花", "胡萝卜", "热狗", "披萨", "甜甜圈", "蛋糕", "椅子", "沙发", "盆栽",
                    "床",
                    "餐桌", "厕所", "电视", "笔记本", "鼠标", "遥控器", "键盘", "手机",
                    "微波炉",
                    "烤箱", "烤面包器", "水池", "冰箱", "书", "时钟", "花瓶", "剪刀", "泰迪熊",
                    "吹风机",
                    "牙刷"]

actual_labels_class = {
    "001": {"name": "动物", "oath": list(range(14, 24))},
    "002": {"name": "植物", "oath": [46, 47, 49, 50, 51] + [58]},
    "003": {"name": "美食", "oath": list(range(46, 56))},
    "004": {"name": "餐具", "oath": list(range(39, 46)) + [60]},
    "005": {"name": "交通", "oath": list(range(9, 13))},
    "006": {"name": "载具", "oath": list(range(1, 9))},
    "007": {"name": "运动", "oath": list(range(29, 39))},
    "008": {"name": "包/箱", "oath": [24, 26, 28, ]},
    "009": {"name": "电器", "oath": list(range(62, 70)) + [72, 74, 78]},
    "010": {"name": "人物", "oath": [0]},
    "011": {"name": "家居", "oath": [79, 78, 76, 75, 61, 60, 59, 57, 13] + list(range(39, 46)) + [60]},
    "012": {"name": "玩具", "oath": [77, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29]},
    "013": {"name": "服装", "oath": [27, 35, ]}
}


def urllib_download():
    global IMAGE_URL
    """
    预下载
    :param IMAGE_URL:
    :return:
    """
    tasks = set()
    names = list()
    import re
    for index, each_url in enumerate(IMAGE_URL):
        image_id = re.findall(r'.+[/\\](.+)\.', each_url)[0]
        names.append(image_id + ".jpg")
        if not os.path.exists(os.path.join("C:/Users/Firefox/PycharmProjects/D/src/", image_id + ".jpg")):
            logging.info("文件{}.jpg下载完毕".format(image_id))
            tasks.add(gevent.spawn(urlretrieve, each_url,
                                   os.path.join("C:/Users/Firefox/PycharmProjects/D/src/", image_id + ".jpg")))
        else:
            logging.warning("{}.jpg已存在,跳过".format(image_id))
    gevent.joinall(tasks)
    return names


all_images_path = []

d.loadModel()
print("model mounted!")


def run_prediction():
    pth = PredictionThread()
    pth.start()
    return pth


def run(urls: list):
    global all_images_path
    global d
    global IMAGE_URL
    before = time.time()

    # with open(r"C:\Users\Firefox\PycharmProjects\E\Interface\record.txt", "rt") as file:
    #     jsonstr = file.readline()
    IMAGE_URL = urls
    image_names = urllib_download()
    pth = run_prediction()
    all_images_path = [os.path.join(abs_image_path, i) for i in image_names]
    output = []
    for index, i in enumerate(all_images_path):
        image = Image.open(i)
        (w, h) = image.size
        try:
            output_array, detections = d.detectObjectsFromImage(
                input_type="array",
                output_type="array",
                input_image=np.array(image),
                minimum_percentage_probability=30)
        except (Exception, IOError):
            logging.CRITICAL("检测出错")
            return
        general_result = []
        maxT = [0, []]  # 建议名称
        for eachObject in detections:
            result = {}
            box = eachObject['box_points']
            percentage_area = (box[3] - box[1]) * (box[2] - box[0]) / w / h  # 百分比面积proportion
            name = eachObject['name']
            label_index = actual_labels.index(name)
            name = actual_labels_cn[label_index]  # 翻译
            result["tag"] = name  # 标签名称
            class_name = []
            for k, v in actual_labels_class.items():
                if label_index in v["oath"]:
                    class_name.append(v['name'])
            if not class_name:
                class_name.append(name)
            result['class'] = class_name  # 所属分类

            result["probability"] = float("{:.2f}".format(eachObject['percentage_probability']))  # 概率

            result["area_proportion"] = percentage_area  # 面积百分比

            a = percentage_area * 0.6 + result['probability'] * 0.4

            if a > maxT[0]:  # 找出建议标签和分类
                maxT[1] = [name, class_name]
            general_result.append(result)
        isNotVoid = True if general_result else False
        res = {
            'index': index + 1,
            'isDetectable': isNotVoid,
            'result': general_result,
            'suggestion': {'tag': maxT[1][0], 'class': maxT[1][1]}
        } if isNotVoid else {
            "index": index + 1,
            "isDetectable": isNotVoid,
            "result": None,
            "suggestion": None
        }
        output.append(res)
    pth.join()  # 等待预测线程结束
    prediction_result = pth.prediction_result
    print(prediction_result)
    print(output)
    for i, v in enumerate(output):
        try:
            if prediction_result and prediction_result[i][1] > 90 and not v["isDetectable"]:
                v["who"] = prediction_result[i][0]
            else:
                v["who"] = None
        except IndexError:
            v["who"] = None
    JsonOutput = {"result": output}
    logging.info("[Detection] Used time: {}".format(time.time() - before))
    return json.dumps(JsonOutput)


class PredictionThread(threading.Thread):
    prediction_result = []

    def init(self):
        threading.Thread.__init__(self)

    def run(self):
        global prediction
        prediction.loadModel()
        for eachPicture in all_images_path:
            if eachPicture.endswith(".png") or eachPicture.endswith(".jpg"):
                predictions, probabilities = prediction.predictImage(eachPicture, result_count=1)
                for each_prediction, percentage_probability in zip(predictions, probabilities):
                    self.prediction_result.append([each_prediction, percentage_probability])

# run()
