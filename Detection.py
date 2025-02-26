import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def object_detect():
    record = 0
    value = -1  # 紀錄 y 座標
    start = False
    state = ""
    image = 2
    array = {0: 0, 1: 0, 2: 0, 3: 0}  # 每個物品最後的統計
    counter = 0  # 用來判斷辨識的第幾張圖片(第一張不考慮)
    now_object = ""  # 現在放入的東西為何物

    array_of_img = []  # this if for store all of the image data

    # this function is for read image,the input is directory name
    def read_directory(directory_name):
        # this loop is for read each image in this foder,directory_name is the foder name with images.
        for filename in os.listdir(directory_name):
            #print(filename) #just for test
            #img is used to store the image data
            img = cv2.imread(directory_name + "/" + filename)
            array_of_img.append(img)

            #print(img)
            print(filename)
            #print(array_of_img)

    net = cv2.dnn.readNetFromDarknet(
        "D:/cfg/yolov3-tiny-obj.cfg",
        "D:/cfg/weights/yolov3-tiny-obj_110000.weights")  #讀模型
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    classes = [line.strip() for line in open("D:/cfg/obj.names")]
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]

    read_directory("C:/xampp/htdocs/AndroidUpload/upload/test/test1")

    for img in array_of_img:
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img,
                                     1 / 255.0, (416, 416), (0, 0, 0),
                                     True,
                                     crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                tx, ty, tw, th, confidence = detection[0:5]
                scores = detection[5:]
                class_id = np.argmax(scores)
                if confidence > 0.5:
                    print("confidence:", confidence)
                    center_x = int(tx * width)
                    center_y = int(ty * height)
                    w = int(tw * width)
                    h = int(th * height)
                    # 取得箱子方框座標
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN

        if (len(boxes) == 0):
            if (start == False):
                print("不考慮")
                continue
            else:
                print("\n空白圖")  #進行統計
                if (start):
                    print("record:", record)
                    array[now_object] += record
                print("Result:", array)
                record = 0
                value = -1
                start = False
                image = 2
                state = "開始"
                now_object = ""
                counter = 0

        for i in range(len(boxes)):
            if i in indexes:
                counter += 1
                if (counter == 1):  #第一張圖不予考慮
                    print("第一張圖不考慮")
                    continue
                x, y, w, h = boxes[i]

                if (boxes[i][1] < 0):
                    boxes[i][1] = 0  #上限
                if (boxes[i][1] > 650):
                    boxes[i][1] = 650  #下限

                if (start == False and image == 2):  #從第2張圖開始辨識(初始化)
                    now_object = class_ids[i]  #放入的是甚麼物品(到結束都是此物品，避免中途失誤)
                    print("NOW_OBJECT:", now_object)
                    value = boxes[i][1]
                    start = True
                elif (image == 3):
                    if (boxes[i][1] > value):
                        state = "放入"
                        record = 1
                    elif (boxes[i][1] < value):
                        state = "取出"
                        record = -1
                else:
                    if (
                            boxes[i][1] > value
                            and (abs(boxes[i][1] - value)) > 10
                    ):  #若y座標的差距超過10，代表有狀態轉換而不是因為物品拿出框格時所造成的誤差(ex: 前:2，後:8，然後拿出)
                        if (state == "取出"):  #取出-->放入
                            record += 1
                        state = "放入"
                    elif (boxes[i][1] < value
                          and (abs(boxes[i][1] - value)) > 10):
                        if (state == "放入"):  #放入-->取出
                            record -= 1
                        state = "取出"

                print("Now :", now_object, classes[now_object])
                print("判斷結果 state:", state, "value:", value)

                value = boxes[i][1]
                image += 1

                print("record:", record)
                print("array:", array)

                label = str(classes[class_ids[i]])
                color = (0, 0, 255)

                cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
                cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
        plt.rcParams['figure.figsize'] = [15, 10]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # plt.subplot(221)
        # plt.imshow(img_rgb)
        # plt.show()
        print("-----------------Next-------------")

    price = [250, 20, 40, 50]
    object = ["Cup", "Milk Tea", "Green Tea", "Brush"]
    Total = 0
    result = ""

    performance = list(array.values())  #每個物品賣出的數量

    for i in range(len(performance)):
        if (performance[i] < 0):
            performance[i] = 0

    for i in array.keys():
        if (array[i] != 0):
            Sum = price[i] * array[i]
            Total = Total + Sum
            result = result + "購賣 " + "%s " % (str(object[i])) + " " + str(
                array[i]) + "個，共" + str(Sum) + "元" + "\n"
            # print("購買 %s %d 個，共%d元" %(classes[i],array[i],Sum),end='')
    result = result + "\n總計" + str(Total) + "元"
    return result, performance, Total


if __name__ == '__main__':
    print(object_detect())
