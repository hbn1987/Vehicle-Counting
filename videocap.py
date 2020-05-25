# -*- coding: UTF-8 -*-
import cv2
import math
from cluster import threshold_cluster

# define blob filter for blob analysing and filtering of bad blobs
class blobz(object):
    def __init__(self, contour):
        self.predictedNextPosition = []
        self.centerPositions = []
        self.currentContour = contour
        self.stillBeingTracked = True
        self.CurrentMatchFoundOrNewBlob = True
        self.haveCounted = False
        self.intNumOfConsecutiveFramesWithoutAMatch = 0
        self.inRecCounter = 0

        x, y, w, h = cv2.boundingRect(contour)
        cx = (2 * x + w) / 2
        cy = (2 * y + h) / 2

        self.centerPositions.append([cx, cy])

    def predictNextPosition(self):
        # next position prediction algorithm based on last 5 weighing sum of tracked blob positions
        numPositions = len(self.centerPositions)
        if (numPositions == 1):
            self.predictedNextPosition = [self.centerPositions[-1][-2], self.centerPositions[-1][-1]]
        if (numPositions == 2):
            deltaX = self.centerPositions[1][0] - self.centerPositions[0][0]
            deltaY = self.centerPositions[1][1] - self.centerPositions[0][1]
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]
        if (numPositions == 3):
            sumOfXChanges = ((self.centerPositions[2][0] - self.centerPositions[1][0]) * 2) + \
                            ((self.centerPositions[1][0] - self.centerPositions[0][0]) * 1)
            deltaX = (sumOfXChanges / 3)
            sumOfYChanges = ((self.centerPositions[2][1] - self.centerPositions[1][1]) * 2) + \
                            ((self.centerPositions[1][1] - self.centerPositions[0][1]) * 1)
            deltaY = (sumOfYChanges / 3)
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]
        if (numPositions == 4):
            sumOfXChanges = ((self.centerPositions[3][0] - self.centerPositions[2][0]) * 3) + \
                            ((self.centerPositions[2][0] - self.centerPositions[1][0]) * 2) + \
                            ((self.centerPositions[1][0] - self.centerPositions[0][0]) * 1)
            deltaX = (sumOfXChanges / 6)
            sumOfYChanges = ((self.centerPositions[3][1] - self.centerPositions[2][1]) * 3) + \
                            ((self.centerPositions[2][1] - self.centerPositions[1][1]) * 2) + \
                            ((self.centerPositions[1][1] - self.centerPositions[0][1]) * 1)
            deltaY = (sumOfYChanges / 6)
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]
        if (numPositions >= 5):
            sumOfXChanges = ((self.centerPositions[numPositions - 1][0] - self.centerPositions[numPositions - 2][0]) * 4) + \
                            ((self.centerPositions[numPositions - 2][0] - self.centerPositions[numPositions - 3][0]) * 3) + \
                            ((self.centerPositions[numPositions - 3][0] - self.centerPositions[numPositions - 4][0]) * 2) + \
                            ((self.centerPositions[numPositions - 4][0] - self.centerPositions[numPositions - 5][0]) * 1)
            sumOfYChanges = ((self.centerPositions[numPositions - 1][1] - self.centerPositions[numPositions - 2][1]) * 4) + \
                            ((self.centerPositions[numPositions - 2][1] - self.centerPositions[numPositions - 3][1]) * 3) + \
                            ((self.centerPositions[numPositions - 3][1] - self.centerPositions[numPositions - 4][1]) * 2) + \
                            ((self.centerPositions[numPositions - 4][1] - self.centerPositions[numPositions - 5][1]) * 1)
            deltaX = (sumOfXChanges / 10)
            deltaY = (sumOfYChanges / 10)
            self.predictedNextPosition = [self.centerPositions[-1][-2] + deltaX, self.centerPositions[-1][-1] + deltaY]

# blob tracking
def matchCurrentFrameBlobsToExistingBlobs(blobs, currentFrameBlobs):
    for existingBlob in blobs:
        existingBlob.CurrentMatchFoundOrNewBlob = False
        existingBlob.predictNextPosition()
    for currentFrameBlob in currentFrameBlobs:
        indexofBlobs = 0
        leastDistance = 1000
        for i in range(len(blobs)):
            if (blobs[i].stillBeingTracked == True):
                diffFrameDis = distance(currentFrameBlob.centerPositions[-1], blobs[i].predictedNextPosition)
                if (diffFrameDis < leastDistance):
                    leastDistance = diffFrameDis
                    indexofBlobs = i
        if (leastDistance < 200):
            blobs = addBlobToExistingBlobs(currentFrameBlob, blobs, indexofBlobs)
        else:
            blobs, currentFrameBlob = addNewBlob(currentFrameBlob, blobs)
    for existingBlob in blobs:
        if (existingBlob.CurrentMatchFoundOrNewBlob == False):
            existingBlob.intNumOfConsecutiveFramesWithoutAMatch = existingBlob.intNumOfConsecutiveFramesWithoutAMatch + 1
        if (existingBlob.intNumOfConsecutiveFramesWithoutAMatch >= 40):
            existingBlob.stillBeingTracked = False
    return blobs

def addBlobToExistingBlobs(currentFrameBlob, blobs, intIndex):
    blobs[intIndex].currentContour = currentFrameBlob.currentContour
    blobs[intIndex].centerPositions.append(currentFrameBlob.centerPositions[-1])
    blobs[intIndex].stillBeingTracked = True
    blobs[intIndex].CurrentMatchFoundOrNewBlob = True
    return blobs

def addNewBlob(currentFrameBlob, blobs):
    currentFrameBlob.CurrentMatchFoundOrNewBlob = True
    blobs.append(currentFrameBlob)
    return blobs, currentFrameBlob

#Draw Blob centre on Image
def drawBlobCentreonImage(blobs,Frame):
    for i in range(len(blobs)):
        if (blobs[i].stillBeingTracked == True):
            if blobs[i].CurrentMatchFoundOrNewBlob == True:
                cv2.circle(Frame, (blobs[i].centerPositions[-1][-2], blobs[i].centerPositions[-1][-1]), 1, (0,255,0), 2)
                cv2.circle(Frame, (blobs[i].centerPositions[-1][-2], blobs[i].centerPositions[-1][-1]),10, (0,255,0), 2)
            else:
                cv2.circle(Frame, (blobs[i].centerPositions[-1][-2], blobs[i].centerPositions[-1][-1]), 1, (0, 100, 0), 2)
                cv2.circle(Frame, (blobs[i].centerPositions[-1][-2], blobs[i].centerPositions[-1][-1]), 10, (0, 100, 0),2)
    return Frame

#Draw Vessel Count On Image
def drawCountOnImage(Count, Frame, frameNo=0):
    initText = " Detected Vessel: "
    #text = initText + str(Count) + " Frame No : " + str(frameNo)
    text = initText + str(Count)
    cv2.putText(Frame, text, (100, Frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
    return Frame

def countCheck(blobs, ver, hor, interval, Count):
    for blob in blobs:
        # # 跨线检测
        # if (blob.stillBeingTracked == True and len(blob.centerPositions) >= 2 and blob.haveCounted == False):
        #     prevFrameIndex= len(blob.centerPositions) - 2
        #     currFrameIndex= len(blob.centerPositions) - 1
        #     if (blob.centerPositions[prevFrameIndex][0] < ver \
        #     and blob.centerPositions[currFrameIndex][0] >= ver):
        #         Count = Count + 1
        #         blob.haveCounted = True
        
        # 方框检测
        if (blob.stillBeingTracked == True and blob.haveCounted == False and blob.CurrentMatchFoundOrNewBlob == True):
            currFrameIndex= len(blob.centerPositions) - 1
            if (blob.centerPositions[currFrameIndex][0] > ver and blob.centerPositions[currFrameIndex][0] < ver + interval \
                and blob.centerPositions[currFrameIndex][1] > hor and blob.centerPositions[currFrameIndex][1] < hor + interval):
                blob.inRecCounter += 1
                if blob.inRecCounter >= 5:
                    Count += 1
                    blob.haveCounted = True
    return Count

def distance(pos1, pos2):
    if (pos2 == []):
        Distance = math.sqrt((pos1[0]) ** 2 + (pos1[1]) ** 2)
    else:
        Distance = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    return Distance

def videocap():
    # 使用cv2.VideoCapture读取视频
    cap = cv2.VideoCapture('./dataset/monitor1.mp4')
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

    while (True):
        ret, Frame = cap.read()
        if not ret:
            break
        frameNo = cap.get(1)
        if frameNo % frameinterval == 0:
            Frame = cv2.resize(Frame, (640, 480))
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
            Count = countCheck(blobs, verticalLine, horizontalLine, interval, Count)
            Frame = drawCountOnImage(Count, Frame, frameNo)
            cv2.imshow('Vessel Counting', Frame)

        firstFrame = False

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 使用cv2.VideoCapture读取视频
    cap = cv2.VideoCapture('./dataset/monitor1.mp4')
    # cv2.getStructuringElement构造形态学使用的kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # 构造高斯混合模型,背景前景分割
    model = cv2.createBackgroundSubtractorMOG2()

    frameinterval = 10
    blobs=[]
    Count=0
    firstFrame = True
    #line
    verticalLine = 500
    horizontalLine = 200
    interval = 130
    
    while(True):
        ret, Frame = cap.read()
        if not ret:
            break
        frameNo = cap.get(1)
        if frameNo % frameinterval == 0:
            Frame = cv2.resize(Frame, (640, 480))
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
            #过滤objs
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
            #合并objs
            if len(objs):
                dislist=[]
                for i in range(len(objs)):
                    dislist.append(distance(objs[0][1], objs[i][1]))
                    index_list, class_list = threshold_cluster(dislist, 300)
                for i in range(len(index_list)):
                    coalobjs.append(objs[index_list[i][0]][0])
            
            curFrameobjs=[]
            for c in range(len(coalobjs)):
                ec=blobz(coalobjs[c]) 
                curFrameobjs.append(ec)
            if (firstFrame ==True) :
                for f1 in curFrameobjs:
                    blobs.append(f1)
            else:
                blobs=matchCurrentFrameBlobsToExistingBlobs(blobs,curFrameobjs)

            Frame = drawBlobCentreonImage(blobs,Frame)
            cv2.rectangle(Frame, (verticalLine, horizontalLine), (verticalLine + interval, horizontalLine + interval), (255, 0 ,0), 2)
            Count = countCheck(blobs, verticalLine, horizontalLine, interval, Count)
            Frame=drawCountOnImage(Count, Frame, frameNo)
            cv2.imshow('Vessel Counting',Frame)
        
        firstFrame = False

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
