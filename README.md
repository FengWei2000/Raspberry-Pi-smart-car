# Raspberry-Pi-smart-car
硬件课程设计，树莓派智能小车。

因为软件代码要和硬件相配合，所以这些代码肯定不能直接使用。但是相信其中的写法会对你有帮助。

computecolor.py计算图片中指定点的HSV值。用于颜色识别阈值的确定。
fire_detection.py火焰检测。
infrad_aviod.py自动避障，用到了红外和超声波。
passive_buzzer.py测试蜂鸣器
server.py服务端，在树莓派上运行，用于与自己的电脑进行socket通信。
testmjpg-2.py两种颜色识别追踪
testmjpg.py一种颜色识别追踪
tracking_2.py自动循迹

以上除了颜色识别是在自己电脑上运行之外，其它都是在树莓派上运行。

# 视频演示地址
[树莓派智能小车功能展示与代码分享](https://www.bilibili.com/video/BV1tv411H7jh)

# 交流
有问题可以提issue
不过提问之前最好先看看这篇文章[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)
