import cv2
import numpy as np  # 导入库
import time
import socket
import sys


# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '10.3.141.1'
port = 2001    		 # 设置端口号
s.connect((host, port))  # 连接服务，指定主机和端口

try:
    black_lower = np.array([110, 64, 100])
    black_upper = np.array([125, 255, 255])  # 设置颜色区间
    blue_lower = np.array([35, 64, 128])
    blue_upper = np.array([55, 255, 255])  # 设置颜色区间
    cap = cv2.VideoCapture("http://10.3.141.1:8080/?action=stream")
    cap.set(3, 640)
    cap.set(4, 480)  # 设置窗口的大小

    tag = None
    while 1:  # 进入无线循环
        t_start = time.time()

        ret, frame = cap.read()  # 将摄像头拍摄到的画面作为frame的值
        frame = cv2.GaussianBlur(frame, (5, 5), 0)  # 高斯滤波GaussianBlur() 让图片模糊
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 将图片的色域转换为HSV的样式 以便检测
        mask = cv2.inRange(hsv, blue_lower, blue_upper)  # 设置阈值，去除背景 保留所设置的颜色
        mask2 = cv2.inRange(hsv, black_lower, black_upper)  # 设置阈值，去除背景 保留所设置的颜色

        mask = cv2.erode(mask, None, iterations=2)  # 显示腐蚀后的图像
        mask = cv2.GaussianBlur(mask, (3, 3), 0)  # 高斯模糊
        mask2 = cv2.erode(mask2, None, iterations=2)  # 显示腐蚀后的图像
        mask2 = cv2.GaussianBlur(mask2, (3, 3), 0)  # 高斯模糊
        res = cv2.bitwise_and(frame, frame, mask=mask)  # 图像合并
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)  # 图像合并
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 边缘检测
        cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # 边缘检测
        if len(cnts) > 0:  # 通过边缘检测来确定所识别物体的位置信息得到相对坐标
            cnt = max(cnts, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)  # 画出一个圆
            print(int(x), int(y))
            print(int(radius))

            if x > 490:
                if tag != 'r':
                    s.sendall('Right'.encode('utf-8'))
                    tag = 'r'
                    print('right')
            elif x < 150:
                if tag != 'l':
                    s.sendall('Left'.encode('utf-8'))
                    tag = 'l'
                    print('left')
            elif radius < 120:
                if tag != 'f':
                    print('forward')
                    s.sendall('Forward'.encode('utf-8'))
                    tag = 'f'
            elif radius > 200:
                if 'tag' != 'b':
                    print('down')
                    s.sendall('Back'.encode('utf-8'))
                    tag = 'b'
            elif tag != 's':
                print('stop')
                s.sendall('Stop'.encode('utf-8'))
                tag = 's'
        elif len(cnts2) > 0:  # 通过边缘检测来确定所识别物体的位置信息得到相对坐标
            cnt = max(cnts2, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)  # 画出一个圆
            print(int(x), int(y))
            print(int(radius))

            if x > 490:
                if tag != 'r':
                    s.sendall('Right'.encode('utf-8'))
                    tag = 'r'
                    print('right')
            elif x < 150:
                if tag != 'l':
                    s.sendall('Left'.encode('utf-8'))
                    tag = 'l'
                    print('left')
            elif radius < 120:
                if tag != 'f':
                    print('forward')
                    s.sendall('Forward'.encode('utf-8'))
                    tag = 'f'
            elif radius > 200:
                if 'tag' != 'b':
                    print('down')
                    s.sendall('Back'.encode('utf-8'))
                    tag = 'b'
            elif tag != 's':
                print('stop')
                s.sendall('Stop'.encode('utf-8'))
                tag = 's'
        else:
            print('stop')
            s.sendall('Stop'.encode('utf-8'))
            tag = 's'
        cv2.imshow('video', frame)  # 将具体的测试效果显示出来
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        if cv2.waitKey(5) & 0xFF == 27:  # 如果按了ESC就退出 当然也可以自己设置
            s.sendall('Stop'.encode('utf-8'))
            print('已经发送停止并且结束程序')
            break
        
        mfps = 1 / (time.time() - t_start)
        print('FPS', mfps)

    cap.release()
    cv2.destroyAllWindows()  # 后面两句是常规操作,每次使用摄像头都需要这样设置一波


except KeyboardInterrupt:
    s.sendall('Stop'.encode('utf-8'))
    print('已经发送停止并且结束程序')
    sys.exit()
