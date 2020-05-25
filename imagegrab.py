# -*- coding: utf-8 -*-
from PIL import ImageGrab
import numpy as np
from videocap import *
from dbmanipulation import processInit, insertIntodb
import time

def imagegrab():
    image = ImageGrab.grab()  # 获得当前屏幕
    width = image.size[0]
    height = image.size[1]
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')# 编码格式
    # video = cv2.VideoWriter('test.avi', fourcc, 25, (width, height))

    # cv2.getStructuringElement构造形态学使用的kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # 构造高斯混合模型,背景前景分割
    model = cv2.createBackgroundSubtractorMOG2()

    frameinterval = 10
    blobs = []
    Count = 0
    firstFrame = True
    # line
    verticalLine = 500
    horizontalLine = 200
    interval = 130

    while True:
        time.sleep(1)
        img_rgb = ImageGrab.grab()
        img_bgr = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        # video.write(img_bgr)

        Frame = cv2.resize(img_bgr, (640, 480))
        # 运用高斯模型进行拟合，在两个标准差内设置为0，在两个标准差外设置为255
        fgmk = model.apply(Frame)
        # 腐蚀、形态学开运算去噪
        fgmk = cv2.erode(fgmk, kernel, iterations=1)
        fgmk = cv2.morphologyEx(fgmk, cv2.MORPH_OPEN, kernel)
        # cv2.findContours计算fgmk的轮廓
        contours = cv2.findContours(fgmk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        objs = dict()
        objindex = 0
        coalobjs = []
        # 过滤objs
        for c in contours:
            # 使用周长进行船的轮廓判断
            length = cv2.arcLength(c, True)
            if length > 150:
                (x, y, w, h) = cv2.boundingRect(c)
                cx = (2 * x + w) / 2
                cy = (2 * y + h) / 2
                centerPosition = [cx, cy]
                objs[objindex] = [c, centerPosition]
                objindex += 1
        # 合并objs
        if len(objs):
            dislist = []
            for i in range(len(objs)):
                dislist.append(distance(objs[0][1], objs[i][1]))
                index_list, class_list = threshold_cluster(dislist, 300)
            for i in range(len(index_list)):
                coalobjs.append(objs[index_list[i][0]][0])

        curFrameobjs = []
        for c in range(len(coalobjs)):
            ec = blobz(coalobjs[c])
            curFrameobjs.append(ec)
        if (firstFrame == True):
            for f1 in curFrameobjs:
                blobs.append(f1)
        else:
            blobs = matchCurrentFrameBlobsToExistingBlobs(blobs, curFrameobjs)

        Frame = drawBlobCentreonImage(blobs, Frame)
        cv2.rectangle(Frame, (verticalLine, horizontalLine), (verticalLine + interval, horizontalLine + interval),
                      (255, 0, 0), 2)
        preCount = Count
        Count = countCheck(blobs, verticalLine, horizontalLine, interval, Count)
        Frame = drawCountOnImage(Count, Frame)

        smallFrame = cv2.resize(Frame, (width / 5, height / 5))
        cv2.imshow('Vessel Counting', smallFrame)
        cv2.moveWindow('Vessel Counting', 0, 0)

        firstFrame = False

        if Count > preCount:
            # 插入操作
            timestamp = int(time.time())
            mydict = {"timeStamp": timestamp, "num": Count - preCount}
            insertIntodb(mydict)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    # video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    processInit()

    image = ImageGrab.grab()# 获得当前屏幕
    width = image.size[0]
    height = image.size[1]
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')# 编码格式
    #video = cv2.VideoWriter('test.avi', fourcc, 25, (width, height))

    # cv2.getStructuringElement构造形态学使用的kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # 构造高斯混合模型,背景前景分割
    model = cv2.createBackgroundSubtractorMOG2()

    frameinterval = 10
    blobs = []
    Count = 0
    firstFrame = True
    # line
    verticalLine = 500
    horizontalLine = 200
    interval = 130

    while True:
        time.sleep(1)
        img_rgb = ImageGrab.grab()
        img_bgr=cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)# 转为opencv的BGR格式
        #video.write(img_bgr)

        Frame = cv2.resize(img_bgr, (640, 480))
        # 运用高斯模型进行拟合，在两个标准差内设置为0，在两个标准差外设置为255
        fgmk = model.apply(Frame)
        # 腐蚀、形态学开运算去噪
        fgmk = cv2.erode(fgmk, kernel, iterations=1)
        fgmk = cv2.morphologyEx(fgmk, cv2.MORPH_OPEN, kernel)
        # cv2.findContours计算fgmk的轮廓
        contours = cv2.findContours(fgmk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        objs = dict()
        objindex = 0
        coalobjs = []
        # 过滤objs
        for c in contours:
            # 使用周长进行船的轮廓判断
            length = cv2.arcLength(c, True)
            if length > 150:
                (x, y, w, h) = cv2.boundingRect(c)
                cx = (2 * x + w) / 2
                cy = (2 * y + h) / 2
                centerPosition = [cx, cy]
                objs[objindex] = [c, centerPosition]
                objindex += 1
        # 合并objs
        if len(objs):
            dislist = []
            for i in range(len(objs)):
                dislist.append(distance(objs[0][1], objs[i][1]))
                index_list, class_list = threshold_cluster(dislist, 300)
            for i in range(len(index_list)):
                coalobjs.append(objs[index_list[i][0]][0])

        curFrameobjs = []
        for c in range(len(coalobjs)):
            ec = blobz(coalobjs[c])
            curFrameobjs.append(ec)
        if (firstFrame == True):
            for f1 in curFrameobjs:
                blobs.append(f1)
        else:
            blobs = matchCurrentFrameBlobsToExistingBlobs(blobs, curFrameobjs)

        Frame = drawBlobCentreonImage(blobs, Frame)
        cv2.rectangle(Frame, (verticalLine, horizontalLine), (verticalLine + interval, horizontalLine + interval),
                      (255, 0, 0), 2)
        preCount = Count
        Count = countCheck(blobs, verticalLine, horizontalLine, interval, Count)
        Frame = drawCountOnImage(Count, Frame)

        smallFrame = cv2.resize(Frame, (width / 5, height / 5))
        cv2.imshow('Vessel Counting', smallFrame)
        cv2.moveWindow('Vessel Counting', 0, 0)

        firstFrame = False

        if Count > preCount:
            # 插入操作
            timestamp = int(time.time())
            mydict = {"timeStamp":timestamp, "num":Count-preCount}
            insertIntodb(mydict)


        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    #video.release()
    cv2.destroyAllWindows()
