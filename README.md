# Channel vessel detection and counting

## main.py: 界面和业务程序调用

## gui.py: 通过pyqt5实现界面

## videocap.py: 船只识别和计数
### step 1: 通过高斯模型进行前景背景分离实现运动目标识别;
### step 2: 通过运动轨迹预测进行运动目标跟踪；
### step 3: 通过记录运动目标在特定区域出现的次数实现运动目标计数。

## imagegrab.py: 录屏功能

## cluster.py: 在目标识别时将距离较近的物体聚合为一个物体

## dbmanipulation.py: 数据库操作

## excelwriter.py: 将结果写入excel

## require: mongodb

## install: 
### step 1: 'pyinstaller main.spec' in cmd 
### step 2: copy 'C:\Python27\Lib\site-packages\PyQt5\*.dll' and 'C:\Python27\Lib\site-packages\PyQt5\plugins\platforms' in the folder which contains 'main.exe'