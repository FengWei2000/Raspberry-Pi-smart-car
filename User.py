import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from TestUI01 import Ui_MainWindow
import cv2
import sys
import socket
import time


class fin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(fin, self).__init__(parent=parent)
        self.setupUi(self)
        self.setStyleSheet("#MainWindow{border-image:url(bg.jpg)}")
        self.setWindowTitle('威天鸣Car')
        self.setWindowIcon(QIcon('icon.ico'))
        icon = QtGui.QPixmap('logo.png').scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio,
                                                Qt.SmoothTransformation)
        self.label.setPixmap(icon)

        self.pushButtonw.clicked.connect(self.on_Forward)
        self.pushButtona.clicked.connect(self.on_Turn_Left)
        self.pushButtons.clicked.connect(self.on_Back)
        self.pushButtond.clicked.connect(self.on_Turn_Right)
        self.pushButton_stop.clicked.connect(self.on_Stop)
        self.spinBox_speed.valueChanged.connect(self.valueChange)
        # 舵机控制
        self.pushButtonUp.clicked.connect(self.Servo_up)
        self.pushButtonDown.clicked.connect(self.Servo_down)
        self.pushButtonLeft.clicked.connect(self.Servo_left)
        self.pushButtonRight.clicked.connect(self.Servo_right)
        self.pushButtonSS.clicked.connect(self.Servo_stop)
        self.pushButton_follow.clicked.connect(self.fire)
        self.pushButton_Connect.clicked.connect(self.connect)

        # # 创建 socket 对象
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = '10.3.141.1'
        # port = 2002  # 设置端口号
        # self.s.connect((host, port))  # 连接服务，指定主机和端口
        # self.timer_camera = QTimer(self)
        # self.cap = cv2.VideoCapture("http://10.3.141.1:8080/?action=stream")
        # self.timer_camera.timeout.connect(self.show_pic)
        # self.timer_camera.start(10)

    def valueChange(self):
        self.s.sendall(str(self.spinBox_speed.value()).encode('utf-8'))

    def connect(self):
        # 创建 socket 对象
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '10.3.141.1'
        port = 2002  # 设置端口号
        # host = 'http://vtmcar.cn.utools.club'
        # port = 2002
        self.s.connect((host, port))  # 连接服务，指定主机和端口
        self.timer_camera = QTimer(self)
        self.cap = cv2.VideoCapture("http://10.3.141.1:8080/?action=stream")
        self.timer_camera.timeout.connect(self.show_pic)
        self.timer_camera.start(10)



    def on_Forward(self):
        self.s.sendall('Forward'.encode('utf-8'))  # 编码方式

    def on_Turn_Left(self):
        self.s.sendall('Left'.encode('utf-8'))  # 编码方式

    def on_Turn_Right(self):
        self.s.sendall('Right'.encode('utf-8'))  # 编码方式

    def on_Back(self):
        self.s.sendall('Back'.encode('utf-8'))  # 编码方式

    def on_Stop(self):
        self.s.sendall('Stop'.encode('utf-8'))  # 编码方式"""

    def Servo_left(self):
        self.s.sendall('SL'.encode('utf-8'))  # 编码方式"""

    def Servo_right(self):
        self.s.sendall('SR'.encode('utf-8'))  # 编码方式"""

    def Servo_up(self):
        self.s.sendall('SU'.encode('utf-8'))  # 编码方式"""

    def Servo_down(self):
        self.s.sendall('SD'.encode('utf-8'))  # 编码方式"""

    def Servo_stop(self):
        self.s.sendall('SS'.encode('utf-8'))  # 编码方式"""


    def show_pic(self):
        success, frame = self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            self.labelView.setPixmap(QPixmap.fromImage(showImage))
            self.labelView.setAlignment(Qt.AlignCenter)
            self.timer_camera.start(10)

    def fire(self):
        try:
            blue_lower = np.array([100, 43, 46])
            blue_upper = np.array([124, 255, 255])  # 设置颜色区间
            cap = cv2.VideoCapture("http://10.3.141.1:8080/?action=stream")
            cap.set(3, 640)
            cap.set(4, 480)  # 设置窗口的大小
            i = 0
            tag = None
            while 1:  # 进入无线循环
                i += 1

                ret, frame = cap.read()  # 将摄像头拍摄到的画面作为frame的值
                frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯滤波GaussianBlur() 让图片模糊
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 将图片的色域转换为HSV的样式 以便检测
                mask = cv2.inRange(hsv, blue_lower, blue_upper)  # 设置阈值，去除背景 保留所设置的颜色

                mask = cv2.erode(mask, None, iterations=2)  # 显示腐蚀后的图像
                mask = cv2.GaussianBlur(mask, (3, 3), 0)  # 高斯模糊
                res = cv2.bitwise_and(frame, frame, mask=mask)  # 图像合并

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 边缘检测

                if i > 10 and len(cnts) > 0:  # 通过边缘检测来确定所识别物体的位置信息得到相对坐标
                    i = 0
                    cnt = max(cnts, key=cv2.contourArea)
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)  # 画出一个圆
                    print(int(x), int(y))
                    print(int(radius))

                    if x > 490:
                        if tag != 'r':
                            self.s.sendall('Right'.encode('utf-8'))
                            tag = 'r'
                            print('right')
                            time.sleep(0.4)
                            self.s.sendall('Stop'.encode('utf-8'))
                            tag = 's'
                    elif x < 150:
                        if tag != 'l':
                            self.s.sendall('Left'.encode('utf-8'))
                            tag = 'l'
                            print('left')
                            time.sleep(0.4)
                            self.s.sendall('Stop'.encode('utf-8'))
                            tag = 's'
                    elif 40 < radius < 120:
                        if tag != 'f':
                            print('forward')
                            self.s.sendall('Forward'.encode('utf-8'))
                            tag = 'f'
                            time.sleep(1)
                            self.s.sendall('Stop'.encode('utf-8'))
                            tag = 's'
                    elif radius > 200 or radius < 40:
                        if 'tag' != 'b':
                            print('down')
                            self.s.sendall('Back'.encode('utf-8'))
                            tag = 'b'
                            time.sleep(1)
                            self.s.sendall('Stop'.encode('utf-8'))
                            tag = 's'
                    elif tag != 's':
                        print('stop')
                        self.s.sendall('Stop'.encode('utf-8'))
                        tag = 's'
                else:
                    pass
                cv2.imshow('video', frame)  # 将具体的测试效果显示出来
                #     cv2.imshow('mask',mask)
                #     cv2.imshow('res',res)
                if cv2.waitKey(5) & 0xFF == 27:  # 如果按了ESC就退出 当然也可以自己设置
                    self.s.sendall('Stop'.encode('utf-8'))
                    print('已经发送停止并且结束程序')
                    break

            cap.release()
            cv2.destroyAllWindows()  # 后面两句是常规操作,每次使用摄像头都需要这样设置一波


        except KeyboardInterrupt:
            self.s.sendall('Stop'.encode('utf-8'))
            print('已经发送停止并且结束程序')
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("loading.png"))
    splash.showMessage("正在加载", QtCore.Qt.AlignHCenter, QtCore.Qt.black)
    splash.show()  # 显示启动界面
    MainWindow = fin()
    MainWindow.show()
    splash.finish(MainWindow)
    sys.exit(app.exec_())
