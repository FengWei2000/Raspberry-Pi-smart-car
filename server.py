# 导入必要的包 
import socket,sys,os 
import time

# import wiringpi,time,multiprocessing 
import RPi.GPIO as GPIO
from Adafruit_PWM_Servo_Driver import PWM

pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000.0                   # 1,000,000 us per second
  pulseLength /= 50.0                       # 60 Hz
  print("%d us per period" % pulseLength)
  pulseLength /= 4096.0                     # 12 bits of resolution
  print("%d us per bit" % pulseLength)
  pulse *= 1000.0
  pulse /= (pulseLength*1.0)
# pwmV=int(pluse)
  print("pluse: %f  " % (pulse))
  pwm.setPWM(channel, 0, int(pulse))


#Angle to PWM
def write(servonum,x):
  y=x/90.0+0.5
  y=max(y,0.5)
  y=min(y,2.5)
  setServoPulse(servonum,y)

pwm.setPWMFreq(50)                        # Set frequency to 50 Hz

PWMA = 18
AIN1   =  22
AIN2   =  27

PWMB = 23
BIN1   = 25
BIN2  =  24
 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2,GPIO.OUT)
GPIO.setup(AIN1,GPIO.OUT)
GPIO.setup(PWMA,GPIO.OUT)

GPIO.setup(BIN1,GPIO.OUT)
GPIO.setup(BIN2,GPIO.OUT)
GPIO.setup(PWMB,GPIO.OUT)

L_Motor= GPIO.PWM(PWMA,100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB,100)
R_Motor.start(0)


 
# 定义小车类及方法 
class Car(object):     
    def __init__(self):         
        self.t_stop(2)

    def t_up(self, speed, t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
    def t_stop(self,t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
    def t_down(self,speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

    def t_left(self,speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

    def t_right(self,speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
    def Servo_left(self,servo_lr):
        if servo_lr>170:
            servo_lr = 175
        else :
            servo_lr += 10
        write(1, servo_lr)
        return servo_lr
    
    def Servo_right(self,servo_lr):
        if servo_lr<30:
            servo_lr = 20
        else :
            servo_lr -= 10
        write(1, servo_lr)
        
        return servo_lr
        

    def Servo_up(self,servo_ud):
        if servo_ud<5:
            servo_ud = 0
        else :
            servo_ud -= 5
        write(2, servo_ud)
        return servo_ud
        

    def Servo_down(self,servo_ud):
        if servo_ud>35:
            servo_ud = 40
        else :
            servo_ud += 5
        write(2, servo_ud)
        
        return servo_ud
        
    
    def Servo_stop(self):
        pwm.setsleep()
        
 
# 使用 socket 进行连接     
def rec_msg(car):
    servo_lr = 90
    servo_ud = 0
    speed = 30
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = '0.0.0.0' 
    port = 2001         # 设置端口号
    print(host)     
    serversocket.bind((host, port)) 
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
 
    while True: 
        rec_msg = clientsocket.recv(1024).decode('utf-8')
        print(rec_msg)
        if rec_msg == "Forward":             
            car.t_up(speed,0)
        elif rec_msg == "Back":             
            car.t_down(speed,0)
        elif rec_msg == "Left":            
            car.t_left(30,0)
        elif rec_msg == "Right":             
            car.t_right(30,0)
        elif rec_msg == "Stop":             
            car.t_stop(0)
        elif rec_msg == "SL":             
            servo_lr = car.Servo_left(servo_lr)
        elif rec_msg == "SR":             
            servo_lr = car.Servo_right(servo_lr)
        elif rec_msg == "SU":            
            servo_ud = car.Servo_up(servo_ud)
        elif rec_msg == "SD":             
            servo_ud =car.Servo_down(servo_ud)
        elif rec_msg == "SS":             
            car.Servo_stop(0)
        elif rec_msg.isdigit():
            speed = eval(rec_msg)
            

# 主函数
if __name__ == "__main__": 
    car = Car()          
    rec_msg(car)