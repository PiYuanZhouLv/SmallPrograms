from random import *
from time import sleep
money = randint(2, 2000)
##money = 10
start = money
def main(sleep_time):
    global money, strat
    print('你的资金：', money)
    times = 0
    get = 0
    put = 0
    get1 = 0
    get2 = 0
    get3 = 0
    get4 = 0
    get5 = 0
    get6 = 0
    gett1 = 0
    gett2 = 0
    gett3 = 0
    gett4 = 0
    gett5 = 0
    gett6 = 0
    while True:
        print()
        sleep(sleep_time)
        red = list(set(input('红球(1-33)(6个或以上，使用空格隔开):').split(' ')))
        if len(red) < 6:
            red = sample([i for i in range(1, 34)], 6)
        blue = list(set(input('蓝球(1-16)(1个或以上，使用空格隔开):').split(' ')))
        if len(blue) == 1 and blue[0] == '':
            blue = sample([i for i in range(1, 17)], 1)
        print('红球：', *red)
        print('蓝球：', *blue)
        sleep(sleep_time)
        need = ((cj(len(red)))/((cj(6))*(cj(len(red)-6))))*len(blue)*2
        print('需花费：', need)
        sleep(sleep_time)
        if need > money:
            print('资金不足！')
            continue
        times += 1
        put += int(need)
        money -= need
        print('剩余资金：', money)
        pool = randint(int(need*0.49), int(need*1000*0.49))*100
        print('奖池资金：', pool)
        ball = summon()
        red_ball = [ball[0], ball[1], ball[2], ball[3], ball[4], ball[5]]
        blue_ball = ball[6]
        red_right = 0
        sleep(sleep_time)
        print('中奖红球：', *red_ball)
        print('中奖蓝球：', blue_ball)
        for i in red:
            if int(i) in red_ball:
                red_right += 1
        blue_right = 0
        for i in blue:
            if int(i) == blue_ball:
                blue_right += 1
        sleep(sleep_time)
        if red_right == 6 and blue_right == 1:
            print('一等奖：', (need*1.5*0.75+pool if need*1.5*0.75+pool < 5000000 else 5000000))
            money += (need*1.5*0.75+pool if need*1.5*0.75+pool < 5000000 else 5000000)
            get1 += (need*1.5*0.75+pool if need*1.5*0.75+pool < 5000000 else 5000000)
            gett1 += 1
            get += (need*1.5*0.75+pool if need*1.5*0.75+pool < 5000000 else 5000000)
        elif red_right == 6 and blue_right == 0:
            print('二等奖：', ((need*1.5*0.75+pool)*0.25 if (need*1.5*0.75+pool)*0.25 < 5000000 else 5000000))
            money += ((need*1.5*0.75+pool)*0.25 if (need*1.5*0.75+pool)*0.25 < 5000000 else 5000000)
            get2 += ((need*1.5*0.75+pool)*0.25 if (need*1.5*0.75+pool)*0.25 < 5000000 else 5000000)
            gett2 += 1
            get += ((need*1.5*0.75+pool)*0.25 if (need*1.5*0.75+pool)*0.25 < 5000000 else 5000000)
        elif red_right == 5 and blue_right == 1:
            print('三等奖：', 3000)
            money += 3000
            get3 += 3000
            gett3 += 1
            get += 3000
        elif (red_right == 5 and blue_right == 0) or (red_right == 4 and blue_right == 1):
            print('四等奖', 200)
            money += 200
            get4 += 200
            gett4 += 1
            get += 200
        elif (red_right == 4 and blue_right == 0) or (red_right == 3 and blue_right == 1):
            print('五等奖', 10)
            money += 10
            get5 += 10
            gett5 += 1
            get += 10
        elif (red_right == 2 and blue_right == 1) or (red_right == 1 and blue_right == 1) or (red_right == 0 and blue_right == 1):
            print('六等奖', 5)
            money += 5
            get6 += 5
            gett6 += 1
            get += 5
        else:
            print('未中奖……')
        print('当前剩余资金：', money)
        if money < 2:
            break
    print('游戏结束'.center(76, '='))
    print(('起始资金：%s     抽奖次数：%s     投资金额：%s     总中奖金额：%s' % (start, times, put, get)).center(60))
    print('┌'+'─'*78+'┐')
    print('│'+'中奖明细'.center(74)+'│')
    tamp = '│'+'{:s}等奖        共 {: >4d} 次        总计 {: >8.2f} 元'.center(77)+'│'
    print(tamp.format('一', gett1, get1))
    print(tamp.format('二', gett2, get2))
    print(tamp.format('三', gett3, get3))
    print(tamp.format('四', gett4, get4))
    print(tamp.format('五', gett5, get5))
    print(tamp.format('六', gett6, get6))
    print('┖'+'─'*78+'┙')
def summon():
    red_ball_list = [i for i in range(1, 34)]
    blue_ball_list = [i for i in range(1, 17)]
    return sample(red_ball_list, 6)+sample(blue_ball_list, 1)
def cj(num):
    an = 1
    for i in range(1, num+1):
        an *= i
    return an
if __name__ == '__main__':
    print('''中奖说明：
一等奖\t6+1\t   \t   \tpool+biggest or 5000000
二等奖\t6+0\t   \t   \t¹/₄(pool+biggest) or 5000000
三等奖\t5+1\t   \t   \t3000
四等奖\t5+0\t4+1\t   \t200
五等奖\t4+0\t3+1\t   \t10
六等奖\t2+1\t1+1\t0+1\t5


''')
    sleep_time = int(input('为了更好的游戏体验，请输入在游戏运行时停顿的时间(单位：秒)：'))
    main(sleep_time)
    while True:
        sleep(1)
