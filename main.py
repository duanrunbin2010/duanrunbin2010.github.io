import sensor
import display
import time
import htd
import bm
import button
import red
import servo
import green
import blue
import black
import white
from machine import I2C
from bno055 import BNO055
from pid import PID
from machine import SoftI2C
from vl53l1x import VL53L1X


foot0 = servo.foot0
arm18 = servo.arm18
arm19 = servo.arm19
darm = servo.darm       #竖直中心调节
dd = servo.dd           #水平中心调节

n = 18
foot1 = [500]*n

red = red.red
green = green.green
blue = blue.blue
black = black.black
white = white.white

blobx = [None]
line1x = [None]
line2x = [None]
def programDev():
    near_blob(foot1, 70, 40, 40, 0, 150, blue)
    c_blob(foot1, 70, 0, 0, 0, 150, blue, dd, 90)
    c_blob(foot1, 70, 0, 0, 0, 150, blue, dd, 80)
    bm.bm1(600)
    time.sleep(1)
    arm(0, 500)
    time.sleep(1)
    leg(1, 500)
    time.sleep(1)
    leg(2, 500)
    time.sleep(1)
    arm(2, 500)
    time.sleep(1)
    line_pace(foot1, 70, 40, 40, 0, 150, 0, 6)
    time.sleep(1)
    #line_pace(foot1, 70, 0, 0, 40, 150, 0, 5)

    line_blob(foot1, 70, 0, 0, 40, 150, 0, blue)
    c_blob(foot1, 70, 0, 0, 0, 150, blue, dd, 90)
    c_blob(foot1, 70, 0, 0, 0, 150, blue, dd, 80)
    arm(0, 500)
    time.sleep(1)
    leg(1, 500)
    time.sleep(1)
    leg(2, 500)
    time.sleep(1)
    arm(2, 500)
    time.sleep(1)
    turn(foot1, 70, 0, 0, 0, 150,300)
    near_blob(foot1, 70, 40, 40, 0, 150, black)
    c_blob(foot1, 70, 0, 0, 0, 150, black, dd, 100)
    bm.bm1(0)

def program1():
   #line_pace29(foot1, 130, 100, 100, 0, 600, 0, 12)
   line_pace(foot1, 70, 0, 0, -40, 150, 0, 4)
   near_blob(foot1, 70, 40, 40, 0, 150, red)    #从远处移动到色块
   catch_ball(foot1, 70, 0, 0, 0, 150, red)

   line_blob(foot1, 70, 0, 0, 60, 150, 0, red)

   catch_ball(foot1, 70, 0, 0, 0, 150, red)

   line_blob(foot1, 70, 0, 0, 60, 150, 0, black)
   Release_ball(foot1, 70, 0, 0, 0, 150, black)

   line_blob(foot1, 70, 0, 0, -60, 150, 0, green)

   catch_ball(foot1, 70, 0, 0, 0, 150, green)

   line_blob(foot1, 70, 0, 0, -60, 150, 0, green)

   catch_ball(foot1, 70, 0, 0, 0, 150, green)

   line_blob(foot1, 70, 0, 0, -60, 150, 0, black)
   Release_ball(foot1, 70, 0, 0, 0, 150, black)

   line2_1(foot1, 70, 0, 0, 60, 150, 0)

   line_pace29(foot1, 130, 100, 100, 0, 600, 0, 13)

   line_pace(foot1, 70, 40, 40, 0, 150,0, 4)    #车身固定在angle方向移动pace步
   line_pace(foot1, 70, 0, 0, 60, 150,0, 3)

   near_blob(foot1, 70, 40, 40, 0, 150, blue)
   catch_ball(foot1, 70, 0, 0, 0, 150, blue)

   near_blob(foot1, 70, 40, 40, 0, 150, blue)
   catch_ball(foot1, 70, 0, 0, 0, 150, blue)

   turn(foot1, 70, 0, 0, 0, 150,270)

   near_blob(foot1, 70, 40, 40, 0, 150, black)
   c_blob(foot1, 70, 0, 0, 0, 150, black, dd, 100)
   bm.bm1(0)
   arm(0, 500)

def program2():
    arm(2, 500)
    time.sleep(2)
    automatic()

def program3():
    arm(1, 500)
    leg(1,500)
    time.sleep(2)
    while True:
        line2()

def Release_ball(data, h, l, r, d, times, code):
    #near_blob(data, h, l, r, d, times, code)
    c_blob(data, h, l, r, d, times, code, dd, 100)
    bm.bm1(0)
    arm(0, 500)
    time.sleep(3)
    arm(2, 500)

def catch_ball(data, h, l, r, d, times, code):
    #near_blob(data, h, l, r, d, times, code)
    c_blob(data, h, l, r, d, times, code, dd, 90)
    c_blob(data, h, l, r, d, times, code, dd, 80)
    bm.bm1(600)
    time.sleep(1)
    arm(0, 500)
    time.sleep(1)
    leg(1, 500)
    time.sleep(1)
    leg(2, 500)
    time.sleep(1)
    arm(2, 500)
    time.sleep(1)

def camera_init():

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QQVGA2)
    sensor.skip_frames(time=2500)

def automatic():                          #自动色块阈值,error取0~15，1键减小，2键增大
    r = [(128 // 2) - (10 // 2), (160 // 2) - (10 // 2), 10, 10]
    arm(2, 500)
    leg(2, 500)
    time.sleep(1)

    def writr_threshold(path, data):
        with open(path,'w+') as f:
            f.write(str(data))

    def prepare():
        c = 0
        while True:
            if button.k1():
                c = c - 1
            if button.k2():
                c = c + 1
            if button.k3():
                break
            if c < 0:
                c = 4
            if c > 4:
                c = 0

            img = sensor.snapshot()
            img.draw_rectangle(r)

            if c == 0:
                img.draw_string(24, 0, 'red', scale=2, color = (255,0,0))
            elif c == 1:
                img.draw_string(24, 0, 'green', scale=2, color = (0,255,0))
            elif c == 2:
                img.draw_string(24, 0, 'blue', scale=2, color = (0,0,255))
            elif c == 3:
                img.draw_string(24, 0, 'black', scale=2, color = (0,0,0))
            elif c == 4:
                img.draw_string(24, 0, 'white', scale=2, color = (255,255,255))

            lcd.write(img, x_scale=-1, y_scale=-1)

        for i in range(60):
            img = sensor.snapshot()
            img.draw_rectangle(r)
            lcd.write(img, x_scale=-1, y_scale=-1)

        threshold = [50, 50, 0, 0, 0, 0]

        for i in range(60):
            img = sensor.snapshot()
            hist = img.get_histogram(roi=r)
            lo = hist.get_percentile(0.01)
            hi = hist.get_percentile(0.99)
            threshold[0] = (threshold[0] + lo.l_value()) // 2
            threshold[1] = (threshold[1] + hi.l_value()) // 2
            threshold[2] = (threshold[2] + lo.a_value()) // 2
            threshold[3] = (threshold[3] + hi.a_value()) // 2
            threshold[4] = (threshold[4] + lo.b_value()) // 2
            threshold[5] = (threshold[5] + hi.b_value()) // 2
            for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, margin=10):
                img.draw_rectangle(blob.rect())
                img.draw_cross(blob.cx(), blob.cy())
                img.draw_rectangle(r)
                lcd.write(img, x_scale=-1, y_scale=-1)

        data = [threshold, c]
        return data

    data = prepare()
    threshold = [0]*6
    for i in range(6):
        threshold[i] = data[0][i]

    er = 0
    while True:
        img = sensor.snapshot()
        for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, margin=10):
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            img.draw_string(24, 120, 'c='+str(data[1]), scale=2)
            img.draw_string(24, 140, 'er='+str(er), scale=2)
            lcd.write(img, x_scale=-1, y_scale=-1)

        if button.k1():
            er = er - 1

        if button.k2():
            er = er + 1

        if button.k3():
            if data[1] == 0:
                writr_threshold('red.py', 'red = '+str(threshold))
            elif data[1] == 1:
                writr_threshold('green.py', 'green = '+str(threshold))
            elif data[1] == 2:
                writr_threshold('blue.py', 'blue = '+str(threshold))
            elif data[1] == 3:
                writr_threshold('black.py', 'black = '+str(threshold))
            elif data[1] == 4:
                writr_threshold('white.py', 'white = '+str(threshold))

            er = 0
            data = prepare()
            threshold = [0]*6
            for i in range(6):
                threshold[i] = data[0][i]

        if er > -2 and er < 20:
            threshold[0] = data[0][0] - er
            threshold[1] = data[0][1] + er
            threshold[2] = data[0][2] - er
            threshold[3] = data[0][3] + er
            threshold[4] = data[0][4] - er
            threshold[5] = data[0][5] + er
        else:
            break

        threshold[0] = max(threshold[0], 0)
        for i in range(6):
            threshold[i] = max(threshold[i], -100)
            threshold[i] = min(threshold[i], 100)

        print(threshold)

    while True:
        c_blob(foot1, 70, 0, 0, 0, 150, red, dd, 90)
        c_blob(foot1, 70, 0, 0, 0, 150, red, dd, 80)
        arm(0, 500)
        time.sleep(1)
        leg(1, 500)
        time.sleep(1)
        leg(2, 500)
        time.sleep(1)
        arm(2, 500)
        time.sleep(1)

def blobs_c(code):
    global blobx
    refresh = False
    img = sensor.snapshot()
    eccentricity_min = 240                #计算到（64，160）的最小偏心距
    for blob in img.find_blobs([code], pixels_threshold=30, area_threshold=30):
        eccentricity = 2*abs(blob.cx()-64)+abs(blob.cy()-80)
        if eccentricity_min > eccentricity:
            eccentricity_min = eccentricity
            blobx = blob
            refresh = True
    if refresh:
        img.draw_rectangle(blobx.rect())
        lcd.write(img, x_scale=-1, y_scale=-1)
    return refresh

def blobs_d(code):
    global blobx
    refresh = False
    img = sensor.snapshot()
    eccentricity_min = 340                #计算到（64，160）的最小偏心距
    for blob in img.find_blobs([code], pixels_threshold=30, area_threshold=30):
        eccentricity = 3*abs(blob.cx()-64)+abs(blob.cy()-160)
        if eccentricity_min > eccentricity:
            eccentricity_min = eccentricity
            blobx = blob
            refresh = True
    if refresh:
        img.draw_rectangle(blobx.rect())
        lcd.write(img, x_scale=-1, y_scale=-1)
    return refresh

def line1():
    global line1x
    refresh = False
    img = sensor.snapshot()
    eccentricity_min = 200
    for l in img.find_lines(x_stride = 5, y_stride = 5, threshold = 500, theta_margin = 25, rho_margin = 25):
        if l.x1() > 0 or l.x2() < 127:     #不能取128
            eccentricity = l.theta()
            if eccentricity > 90:
                eccentricity = eccentricity - 180
            eccentricity = abs(eccentricity)+abs(l.x1()+l.x2()-128)
            if eccentricity_min > eccentricity:
                eccentricity_min = eccentricity
                line1x = l
                refresh = True
    if refresh:
        img.draw_line(line1x.line(), color=(255, 0, 0))
        lcd.write(img, x_scale=-1, y_scale=-1)
    return refresh

def line2():
    global line2x
    refresh = False
    img = sensor.snapshot()
    eccentricity_min = 200
    for l in img.find_lines(x_stride = 5, y_stride = 5, threshold = 500, theta_margin = 25, rho_margin = 25):
        if l.y1() > 0 or l.y2() < 159:     #不能取160
            eccentricity = l.theta()-90
            eccentricity = abs(eccentricity)+abs(160-l.y1()-l.y2())
            if eccentricity_min > eccentricity:
                eccentricity_min = eccentricity
                line2x = l
                refresh = True
    if refresh:
        img.draw_line(line2x.line(), color=(255, 0, 0))
        lcd.write(img, x_scale=-1, y_scale=-1)
    return refresh

def dyaw(angle):                           #计算指定角度与当前航向角的偏差
    global imu
    deviation = angle - imu.euler()[0]
    if deviation > 180:
        deviation = deviation - 360
    elif deviation < -180:
        deviation = deviation + 360
    if deviation == 0 or (deviation > 0 and pid_yaw._integrator < 0) or (deviation < 0 and pid_yaw._integrator > 0):
        pid_yaw.reset_I()
    return round(pid_yaw.get_pid(deviation, 1))

def turn(data, h, l, r, d, times, angle):
    global imu
    global pid_yaw
    pid_yaw._ki = 0
    while True:
        da = dyaw(angle)
        if abs(da) < 5:
            pid_yaw._ki = 1.3
            break
        da = 5*da
        da = max(da, -50)
        da = min(da, 50)
        if l == 0 and r == 0 and d == 0:
            htd.move(data, h, da, -da, 0, times)
        else:
            htd.move(data, h, l, r, d, times)

def line_pace(data, h, l, r, d, times, angle, pace):    #车身固定在angle方向移动pace步
    for i in range(pace):
        da = dyaw(angle)
        da = max(da, -40)
        da = min(da, 40)
        htd.move(data, h, l+da, r-da, d, times)

def line_blob(data, h, l, r, d, times, angle, code):    #车身固定在angle方向移动到指定色块
    while True:
        refresh = blobs_c(code)
        da = dyaw(angle)
        da = max(da, -40)
        da = min(da, 40)
        htd.move(data, h, l+da, r-da, d, times)
        if refresh and blobs_c(code) and blobx.cx() > 34 and blobx.cx() < 94 and blobx.cy() > 20 and blobx.cy() < 140:
            break

def line1_2(data, h, l, r, d, times, angle):          #车身固定在angle方向移动到横线
     while True:
        refresh = line2()
        da = dyaw(angle)
        da = max(da, -40)
        da = min(da, 40)
        htd.move(data, h, l+da, r-da, d, times)
        if refresh and line2() and abs(line2x.y1()+line2x.y2()-160) < 40:
            break

def line2_1(data, h, l, r, d, times, angle):         #车身固定在angle方向移动到竖线
     while True:
        refresh = line1()
        da = dyaw(angle)
        da = max(da, -40)
        da = min(da, 40)
        htd.move(data, h, l+da, r-da, d, times)
        if refresh and line1() and abs(line1x.x1()+line1x.x2()-128) < 40:
            break
def line_pace29(data, h, l, r, d, times, angle, pace):
    leg(1, 500)
    arm(2, 500)
    line_pace1(data, h, l, r, d, times, angle, pace)
    while True:
        if imu.euler()[2] > -5:
            break
        line_pace1(data, h, l, r, d, times, angle, 1)
    leg(2, 500)
    arm(2, 500)
    #line1_2(data, h, l, r, d, times, angle)
    #line_blob(data, h, l, r, d, times, angle, blue)
    #line1_2(data, h, l, r, d, times, angle)
    #
    #line_pace1(data, h, l, r, d, times, angle, 1)

def line_pace1(data, h, l, r, d, times, angle, pace):    #车身固定在angle方向骑黑线移动pace步
    for i in range(pace):
        da = dyaw(angle)
        da = max(da, -40)
        da = min(da, 40)
        refresh = line1()
        if refresh:
            dx = (line1x.x1()+line1x.x2()-128)
            dx = max(dx, -40)
            dx = min(dx, 40)
        else:
            dx = 0
        htd.move(data, h, l+da, r-da, d+dx, times)
def t1_blob(data, h, l, r, d, times, code):
    while True:
        refresh = blobs_c(code)
        if line1():
            da = line1x.theta()
            if da > 90:
                da = da - 180
            dx = (line1x.x1()+line1x.x2()-128)//3
            da = max(da, -40)
            da = min(da, 40)
            dx = max(dx, -40)
            dx = min(dx, 40)
        else:
            da = 0
            dx = 0
        htd.move(data, h, l+da, r-da, d+dx, times)
        if refresh and blobs_c(code):
            break

def t2_blob(data, h, l, r, d, times, code):
    while True:
        refresh = blobs_c(code)
        if line2():
            da = line2x.theta()-90
            dy = (160-line2x.y1()-line2x.y2())//3
            da = max(da, -40)
            da = min(da, 40)
            dy = max(dy, -40)
            dy = min(dy, 40)
        else:
            da = 0
            dy = 0
        htd.move(data, h, l+dy+da, r+dy-da, d, times)
        if refresh and blobs_c(code):
            break

def c_blob(data, h, l, r, d, times, code, x, y):  #从近处移动到色块
    global blobx
    i = 0
    count1 = 0
    count2 = 0
    while True:
        refresh = blobs_c(code)
        if refresh:
            dx = blobx.cx()-x
            dx = 3*dx//2
            dx = max(dx, -40)
            dx = min(dx, 40)
            dy = y-blobx.cy()
            dy = 3*dy//2
            dy = max(dy, -40)
            dy = min(dy, 40)
        else:
            dx = 0
            dy = 0
        htd.movex(data, h, l+dy+dx, r+dy-dx, d+dx, times, i+1)

        if dx > -10 and dx < 10  and dy > -10 and dy < 10:
            if (count1 > 3 and count2 > 5) or count2 > 20:
                if refresh and blobs_d(code):
                    return blobx.code()
            else:
                count1 = count1 + 1
        else:
            count1 = 0
        count2 = count2 + 1
        i = i + 1
        if i > 3:
            i = 0

def near_blob(data, h, l, r, d, times, code):    #从远处移动到色块
    global blobx
    arm(3, 200)
    time.sleep(1)
    while True:
        refresh = blobs_d(code)
        if refresh:
            dx = blobx.cx()-64
            dx = max(dx, -40)
            dx = min(dx, 40)
        else:
            dx = 0
        htd.move(data, h, l+dx, r-dx, d+dx, times)
        if refresh and blobs_d(code) and blobx.cy() > 120:
            arm(2, 200)
            time.sleep(1)
            return blobx.code()

def c_line1(data, h, l, r, d, times):
    global line1x
    i = 0
    count1 = 0
    count2 = 0
    while True:
        refresh = line1()
        if line1x:
            da = line1x.theta()
            if da > 90:
                da = da - 180
            da = max(da, -40)
            da = min(da, 40)
            dx = line1x.x1()+line1x.x2()-128
            dx = max(dx, -40)
            dx = min(dx, 40)
        else:
            dx = 0
            da = 0
        htd.movex(data, h, l+da, r-da, d+dx, times, i+1)
        if dx > -10 and dx < 10  and da > -3 and da < 3:
            if (count1 > 3 and count2 > 5) or count2 > 20:
                if refresh and line1():
                    return line1x
            else:
                count1 = count1 + 1
        else:
            count1 = 0
        count2 = count2 + 1
        i = i + 1
        if i > 3:
            i = 0

def c_line2(data, h, l, r, d, times):
    global line2x
    i = 0
    count1 = 0
    count2 = 0
    while True:
        refresh = line2()
        if line2x:
            da = line2x.theta()-90
            da = max(da, -40)
            da = min(da, 40)
        else:
            da = 0
        htd.movex(data, h, l+da, r-da, d, times, i+1)
        if da > -3 and da < 3:
            if (count1 > 3 and count2 > 5) or count2 > 20:
                if refresh and line2():
                    return line2x
            else:
                count1 = count1 + 1
        else:
            count1 = 0
        count2 = count2 + 1
        i = i + 1
        if i > 3:
            i = 0

def arm1(angle, times):
    angle = max(angle, 0)
    angle = min(angle, 500)
    htd.servo_htd(18, arm18+angle, times)      #机械臂第一关节，看远darm+300,看近darm，水平高位250，水平低位0

def arm2(angle, times):
    angle = max(angle, -250)
    angle = min(angle, 0)
    htd.servo_htd(19, arm19+angle, times)      #机械臂第二关节，水平高位-250，收缩和水平低位0

def arm(s, times):                                  #低位0高位1看近2看远3收缩4
    global darm
    if s == 0:
        arm1(0, times)
        arm2(0, times)
    elif s == 1:
        arm1(250, times)
        arm2(-250, times)
    elif s == 2:
        arm1(darm, times)
        arm2(-250, times)
    elif s == 3:
        arm1(darm+300, times)
        arm2(-250, times)
    elif s == 4:
        arm1(450, times)
        arm2(0, times)

def leg(s, times):
    if s == 0:
        htd.gait(foot0, foot1, 0, 0, 0, times)
    if s == 1:
        htd.gait(foot0, foot1, 100, 120, 0, times)
    if s == 2:
        htd.gait(foot0, foot1, 100, 300, -180, times)
    if s == 3:
        htd.gait(foot0, foot1, 100, 400, -280, times)

pid_yaw = PID(p=1, i=1, d=0, imax=50)  #航向角pid

bm.bm_init()

lcd = display.SPIDisplay(bgr = True, triple_buffer=True)
lcd.backlight(25)

imu_i2c = I2C(2)
imu = BNO055(imu_i2c, mode = 8)   #航向角yaw：0~359度，顺时针增大

laser_i2c = SoftI2C(scl='D14', sda='D15')
#distance = VL53L1X(laser_i2c)    #激光测距初始化

def main():            #主程序
    global imu
    global blobx
    clock = time.clock()
    arm(2, 500)        #读取舵机数据时可以注释掉
    leg(2, 500)        #读取舵机数据时可以注释掉
    time.sleep(2)
    camera_init()
    time.sleep(1)
    img = sensor.snapshot()
    lcd.write(img, x_scale=-1, y_scale=-1)
    arm(4, 500)
    while True:
        clock.tick()
        img = sensor.snapshot()
        img.draw_string(24, 0, str(int(imu.euler()[2])), scale=2, color = (255,255,255))
        lcd.write(img, x_scale=-1, y_scale=-1)
        if button.k1():
            time_start = time.time()
            imu = BNO055(imu_i2c, mode = 8)
            program1()
            time_end = time.time()
            img.clear()
            img.draw_string(24, 0, 't=', scale=2, color = (255,255,255))
            img.draw_string(24, 30, str(time_end - time_start), scale=2, color = (255,255,255))
            lcd.write(img, x_scale=-1, y_scale=-1)
        if button.k2():
            time_start = time.time()
            imu = BNO055(imu_i2c, mode = 8)
            program2()
            time_end = time.time()
            img.clear()
            img.draw_string(24, 0, 't=', scale=2, color = (255,255,255))
            img.draw_string(24, 30, str(time_end - time_start), scale=2, color = (255,255,255))
            lcd.write(img, x_scale=-1, y_scale=-1)
        if button.k3():
            time_start = time.time()
            imu = BNO055(imu_i2c, mode = 8)
            program3()
            time_end = time.time()
            img.clear()
            img.draw_string(24, 0, 't=', scale=2, color = (255,255,255))
            img.draw_string(24, 30, str(time_end - time_start), scale=2, color = (255,255,255))
            lcd.write(img, x_scale=-1, y_scale=-1)

        print(clock.fps())

if __name__ == '__main__':
    main()
