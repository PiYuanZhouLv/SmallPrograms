import random
import pygame
import csv
import math
# import time

"""
游戏流程：
提示文字阶段 --> 玩家操作阶段 --> 游戏结束  <-------------------------------------------
                  /\                                                                    |
/-----------------  ------------------------------------------------------------\       |
玩家实例 --创建-> 子弹实例 --判断:击中物体-> 进行扣血 --血量为零-> 子弹消失、实例消失/游戏结束 ----
   |               |                                                      ^
   |               |_______________判断:未击中物体________________________|
   ---移动、旋转等事件
！注意：由于使用了get_pressed方法，该游戏暂不支持2.2及以后版本的pygame
"""



pygame.init()
size = width, height = 600, 360
screen = pygame.display.set_mode(size)
pygame.display.set_caption('坦克大战')

no_map_bg = pygame.image.load('assets/images/no_map_bg.png')

sub_scr1 = pygame.Surface((width / 2, height))
sub_scr2 = pygame.Surface((width / 2, height))
my_map = csv.reader(open('assets/maps/map.csv', encoding='utf-8'))
new_map = []
for i in my_map:           # \
    nl = []                # |
    for j in i:            #  > 将csv中以字符串形式保存的数字改为整型
        nl.append(int(j))  # |
    new_map.append(nl)     # |
my_map = new_map           #/

brick0 = pygame.image.load('assets/images/brick0.png')
brick1 = pygame.image.load('assets/images/brick1.png')
brick2 = pygame.image.load('assets/images/brick2.png')
brick3 = pygame.image.load('assets/images/brick3.png')
grass = pygame.image.load('assets/images/grass.png')
floor = pygame.image.load('assets/images/floor.png')
wall = pygame.image.load('assets/images/wall.png')


# sub_scr1.fill('red')
# sub_scr2.fill('green')

class Void:
    ...


def add_text(surface: pygame.Surface, text_, center, f_size, color_='black', font=None, bold=False, italic=False):
    """
    将文本打在屏幕上
    :param surface: 屏幕
    :param text_: 打印的文本
    :param center: 文本中心
    :param f_size: 字体大小
    :param color_: 颜色
    :param font: 字体
    :param bold: 是否加粗
    :param italic: 是否斜体
    :return: 无
    """
    font = pygame.font.SysFont(font, f_size, bold, italic)
    text_surface = font.render(text_, True, color_)
    text_rect = text_surface.get_rect()
    dx, dy = text_rect.center
    surface.blit(text_surface, (center[0] - dx, center[1] - dy))


def make_map(my_map_) -> pygame.Surface:
    """
    构建初始地图
    :param my_map_: 地图
    :return: 构建好的地图
    """
    map_surf_ = pygame.Surface((1600, 1600))
    for i_, tmp_ in enumerate(my_map_):  # enumerate函数，将列表的序号与值相结合：
        for j_, block_ in enumerate(tmp_):  # enumerate([1, 'a', True, ()]) --> ((0, 1), (1, 'a'), (2, True), (3, ()))
            if block_ == 0:
                map_surf_.blit(floor, (j_ * 32, i_ * 32))
            elif block_ == 1:
                map_surf_.blit(grass, (j_ * 32, i_ * 32))
            elif int(block_) == 2:
                if block_ == 2.0:
                    map_surf_.blit(brick0, (j_ * 32, i_ * 32))
                elif block_ == 2.1:
                    map_surf_.blit(brick1, (j_ * 32, i_ * 32))
                elif block_ == 2.2:
                    map_surf_.blit(brick2, (j_ * 32, i_ * 32))
                elif block_ == 2.3:
                    map_surf_.blit(brick3, (j_ * 32, i_ * 32))
            elif block_ == 3:
                map_surf_.blit(wall, (j_ * 32, i_ * 32))

    return map_surf_


map_surf = make_map(my_map)


class Brick:
    pos = [..., ...]  # 砖块的位置
    degree = 0  # 砖块的损毁程度
    life = 40  # 砖块血量

    def __init__(self, pos):
        """
        砖块类
        :param pos:
        """
        self.pos = pos

    def hit(self, effort):
        """
        当砖块被击中时调用
        :param effort: 扣除的血量
        :return: 无
        """
        self.life -= effort
        degree = self.get_degree()
        if degree != self.degree:
            if degree == 1:
                map_surf.blit(brick1, (self.pos[0] * 32, self.pos[1] * 32))
            elif degree == 2:
                map_surf.blit(brick2, (self.pos[0] * 32, self.pos[1] * 32))
            elif degree == 3:
                map_surf.blit(brick3, (self.pos[0] * 32, self.pos[1] * 32))
            else:
                map_surf.blit(floor, (self.pos[0] * 32, self.pos[1] * 32))
                bricks[self.pos[0]].pop(self.pos[1])
            self.degree = degree

    def get_degree(self):
        """
        获取损毁程度的方法
        :return: 当前损毁程度
        """
        return (40 - self.life) // 10


bricks = {}  # 砖块的字典，在第i行、第j列的砖块应用：bricks[j][i]
walls = {}  # 墙的字典，类似于砖块
empty = []  # 空位的列表，用于随机起始点
for i, tmp in enumerate(my_map):
    for j, block in enumerate(tmp):
        if block == 2:
            bricks[j] = bricks.get(j, {})
            bricks[j][i] = Brick((j, i))
        elif block == 3:
            walls[j] = walls.get(j, {})
            walls[j][i] = ...
        else:
            empty.append((j * 32 + 16, i * 32 + 16))


class Bullet:
    B0 = (pygame.transform.scale2x(pygame.image.load(f'assets/images/b00.png')),  # player0 的子弹贴图
          pygame.transform.scale2x(pygame.image.load(f'assets/images/b01.png')),  # scale2x用于将图片放大到原来的两倍
          pygame.transform.scale2x(pygame.image.load(f'assets/images/b02.png')))
    B1 = (pygame.transform.scale2x(pygame.image.load(f'assets/images/b10.png')),  # player1 的
          pygame.transform.scale2x(pygame.image.load(f'assets/images/b11.png')),
          pygame.transform.scale2x(pygame.image.load(f'assets/images/b12.png')))
    surf0 = ...
    surf1 = ...
    surf2 = ...
    en_num = ...
    pos = [..., ...]
    speed = [..., ...]
    left = ...
    effort = ...
    hit = False  # 子弹是否击中目标
    frame_after_hit = 0  # 当前是子弹击中目标后的第几帧(用于播放动画)

    def __init__(self, pos, angle, v_angle, v, num, left, effort, speed_up, cannot_ud, cannot_lr):
        """
        子弹类
        :param pos: 发射位置
        :param angle: 发射角度
        :param v_angle: 速度的角度(用于支持相对论)
        :param v: 速度的大小
        :param num: 发射子弹的玩家的编号
        :param left: 剩余多少帧落地
        :param effort: 打掉对象多少点血
        :param speed_up: [保留]用于子弹加/减速道具
        :param cannot_ud: 不能上下移动时为True (修复蹭墙时发射子弹，子弹角度异常的现象)
        :param cannot_lr: 不能左右移动时为True
        """
        # print('a new bullet')
        # print('pos', pos)
        # print('angle', angle)
        # print('v_angle', v_angle)
        # print('v', v)
        self.surf0, self.surf1, self.surf2 = Bullet.B1 if num else Bullet.B0
        self.pos = pos
        self.speed = [math.sin(angle / 360 * 2 * math.pi) * 1.5 * -speed_up
                      + math.sin(v_angle / 360 * 2 * math.pi) * -v * (not cannot_lr),  # 相对论!!!
                      math.cos(angle / 360 * 2 * math.pi) * 1.5 * -speed_up
                      + math.cos(v_angle / 360 * 2 * math.pi) * -v * (not cannot_ud)]  # 相对论!!!
        # print('speed', self.speed)
        self.left = left
        self.effort = effort
        self.en_num = int(not num)
        bullets.append(self)

    def move(self):
        """
        子弹的移动事件，每一帧触发一次
        :return: 无
        """
        if not self.hit:
            self.pos[0] += self.speed[0]
            self.pos[1] += self.speed[1]
            self.left -= 1
            if walls.get(int(self.pos[0] / 32), {}).get(int(self.pos[1] / 32), None):
                # print('hit wall at', self.pos)
                self.hit = True
            elif bricks.get(int(self.pos[0] / 32), {}).get(int(self.pos[1] / 32), None):
                # For 3.8 or later, just use
                # elif walls.get(int(self.pos[0])+1, {}).get(int(self.pos[1])+1, None) -> hit_brick:
                # print('hit brick at', self.pos)
                hit_brick = bricks[int(self.pos[0] / 32)][int(self.pos[1] / 32)]
                hit_brick.hit(self.effort)
                self.hit = True
            elif (self.en_num == 0
                  and player0.area[0][0] < self.pos[0] < player0.area[1][0]
                  and player0.area[0][1] < self.pos[1] < player0.area[1][1]):
                # print('hit player0 at', self.pos, f'(player0{player0.area})')
                player0.hit(self.effort)
                self.hit = True
            elif (self.en_num == 1
                  and player1.area[0][0] < self.pos[0] < player1.area[1][0]
                  and player1.area[0][1] < self.pos[1] < player1.area[1][1]):
                # print('hit player1 at', self.pos, f'(player1{player1.area})')
                player1.hit(self.effort)
                self.hit = True
            elif self.left <= 0:
                # print('hit ground at', self.pos)
                self.hit = True
        else:
            self.after_hit()

    def render(self):
        """
        渲染方法
        :return: (渲染图, 子弹绝对位置)
        """
        if not self.hit:
            return self.surf0, self.pos
        else:
            if self.frame_after_hit // 15 == 0:
                return self.surf1, self.pos
            else:
                return self.surf2, self.pos

    def after_hit(self):
        """
        子弹击中后，每一帧触发一次(代替move方法)
        :return:
        """
        self.frame_after_hit += 1
        if self.frame_after_hit > 30:
            # print('my life is over, bye')
            bullets.remove(self)


bullets = []  # 子弹列表


def move_inlegal(pos, d):
    """
    检测移动是否合法
    :param pos: 玩家中心
    :param d: 偏移量
    :return: True / False
    """
    return (bricks.get(int((pos[0] + d[0]) / 32), {}).get(int((pos[1] + d[1]) / 32), None)
            or walls.get(int((pos[0] + d[0]) / 32), {}).get(int((pos[1] + d[1]) / 32), None)
            or (pos[0] + d[0]) < 0 or (pos[0] + d[0]) > 1600 or (pos[1] + d[1]) < 0 or (pos[1] + d[1]) > 1600)


class Player:
    pos = [..., ...]
    base_rotate = 0
    gun_rotate = 0
    sub_scr = ...
    keys = [...] * 7
    life = 100  # 玩家生命
    size = [32, 32]
    area = [(..., ...), (..., ...)]
    v = 0  # 玩家速度
    effort = 0  # 玩家打出的伤害
    left = 0  # 玩家打出的子弹还有多少帧落地
    f = 0  # 玩家按住 R/P 键的帧数
    cannot_ud = False  # 玩家不能上下移动时为True
    cannot_lr = False  # ......左右移动........(同上)

    def __init__(self, sub_scr: pygame.Surface, num, keys, pos):
        """
        玩家类
        :param sub_scr: 玩家对应的子屏幕
        :param num: 玩家编号
        :param keys: 玩家按键
        :param pos: 玩家初始位置
        """
        self.enemy = Void()
        self.sub_scr = sub_scr
        self.base = pygame.image.load(f'assets/images/tb{num}.png')
        self.gun = pygame.image.load(f'assets/images/tt{num}.png')
        self.keys = keys
        self.pos = pos
        self.num = num

    def main_event(self):
        """
        每帧触发一次的事件，顺带处理一下渲染Ⅰ阶段
        :return: 同渲染Ⅰ阶段
        """
        self.v = 0  # 重置速度
        self.cannot_ud = self.cannot_lr = False  # 重置运动状态
        kp = pygame.key.get_pressed()  # 由于pygame的原因，这个方法无法在2.2及以后使用
        if kp[self.keys[1]]:  # S/K: go backward
            self.pos[1] += math.cos(self.base_rotate / 360 * 2 * math.pi)
            for d in [(-16, -16), (16, -16), (-16, 16), (16, 16)]:  # 判断四个顶点是否合法
                if move_inlegal(self.pos, d):
                    self.pos[1] -= math.cos(self.base_rotate / 360 * 2 * math.pi)  # 不合法时撤回移动，将对应cannot变量设为True
                    self.cannot_ud = True
                    break
            self.pos[0] += math.sin(self.base_rotate / 360 * 2 * math.pi)
            for d in [(-16, -16), (16, -16), (-16, 16), (16, 16)]:
                if move_inlegal(self.pos, d):
                    self.pos[0] -= math.sin(self.base_rotate / 360 * 2 * math.pi)
                    self.cannot_lr = True
                    break
            self.v = -1
        if kp[self.keys[0]]:  # W/I: go forward
            self.pos[1] -= math.cos(self.base_rotate / 360 * 2 * math.pi)
            for d in [(-16, -16), (16, -16), (-16, 16), (16, 16)]:
                if move_inlegal(self.pos, d):
                    self.pos[1] += math.cos(self.base_rotate / 360 * 2 * math.pi)
                    self.cannot_ud = True
                    break
            self.pos[0] -= math.sin(self.base_rotate / 360 * 2 * math.pi)
            for d in [(-16, -16), (16, -16), (-16, 16), (16, 16)]:
                if move_inlegal(self.pos, d):
                    self.pos[0] += math.sin(self.base_rotate / 360 * 2 * math.pi)
                    self.cannot_lr = True
                    break
            self.v = 1
        if kp[self.keys[3]]:  # Q/U: gun turn left
            self.gun_rotate -= 1
            self.gun_rotate %= 360
        if kp[self.keys[2]]:  # E/O: gun turn right
            self.gun_rotate += 1
            self.gun_rotate %= 360
        if kp[self.keys[5]]:  # A/J: base turn left
            self.base_rotate -= 1
            self.base_rotate %= 360
        if kp[self.keys[4]]:  # D/L: base turn right
            self.base_rotate += 1
            self.base_rotate %= 360
        if kp[self.keys[6]]:  # R/P: shoot!
            self.f += 1
            self.effort = 20 * abs(math.sin(self.f / 120 * math.pi))  # 为了简化公式，直接用 正弦函数《加个绝对值》
            self.left = int(300 * abs(math.sin(self.f / 120 * math.pi)))
        return self.main_display1()  # 顺带调用一下渲染Ⅰ阶段

    def main_display1(self):
        """
        渲染Ⅰ阶段
        这个阶段不会更改屏幕上的内容，而是将自己渲染好，递交给主程序，等待渲染Ⅱ阶段
        :return: (你的渲染图, 你的绝对坐标)
        """
        tmp_surf = pygame.Surface((300, 360))
        tmp_surf.set_colorkey((0, 0, 0))
        tmp_surf.convert_alpha()
        tb = pygame.transform.rotate(self.base, self.base_rotate)
        tbw, tbh = tb.get_rect().center
        tmp_surf.blit(tb, (150 - tbw, 180 - tbh))
        tg = pygame.transform.rotate(self.gun, self.base_rotate + self.gun_rotate)
        tbw, tbh = tg.get_rect().center
        tmp_surf.blit(tg, (150 - tbw, 180 - tbh))
        # self.size = [max(tb.get_rect().w, tg.get_rect().w),
        #              max(tb.get_rect().h, tg.get_rect().h)]
        self.area = [(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2),
                     (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2)]
        # print(self.pos, self.size, self.area)
        return tmp_surf, self.pos

    def main_display2(self, my_surf, en_surf, en_pos, bullets_list):
        """
        渲染Ⅱ阶段
        这个阶段，程序会更新屏幕上的内容，包括：你自己、敌人、子弹、地图。
        :param my_surf: 你自己的渲染图
        :param en_surf: 敌人的渲染图
        :param en_pos: 敌人的绝对坐标
        :param bullets_list: 子弹列表，格式为[(子弹的渲染图, 子弹的绝对坐标), ...]
        :return: 无
        """
        self.sub_scr.blit(map_surf, (-self.pos[0] + 150, -self.pos[1] + 180))  # 渲染地图
        tbw, tbh = my_surf.get_rect().center
        self.sub_scr.blit(my_surf, (150 - tbw, 180 - tbh))  # 渲染你自己
        self.sub_scr.blit(en_surf, (-self.pos[0] + en_pos[0], -self.pos[1] + en_pos[1]))  # 渲染敌人
        for b in bullets_list:
            surf, pos = b
            self.sub_scr.blit(surf, (pos[0] - self.pos[0] + 150 - 8, pos[1] - self.pos[1] + 180 - 8))  # 渲染子弹
        pygame.draw.rect(self.sub_scr, (255, 255, 255, 150), ((0, 0), (300, 20)))  #  画血量条的背景
        pygame.draw.rect(self.sub_scr,
                         (['red', (255, 165, 0), 'yellow', 'yellowgreen', 'green', 'green']  # 画血量条的边框
                          [int(self.life // 20) if self.life > 0 else 0]),
                         ((0, 0), (300, 20)), 1)
        pygame.draw.rect(self.sub_scr,
                         (['red', (255, 165, 0), 'yellow', 'yellowgreen', 'green', 'green']  # 画血量条的色带
                          [int(self.life // 20) if self.life > 0 else 0]),
                         ((0, 0), (300 * self.life / 100, 20)))
        add_text(self.sub_scr, f'{self.life:.2f}' if self.life > 0 else 'dead', (150, 10), 20,  # 添加血量显示
                 'black' if self.life >= 20 else 'red')
        if self.f:
            pygame.draw.rect(self.sub_scr, 'skyblue', ((0, 20), (300, 10)), 1)  # 如果在蓄力，则画出蓄力条的边框...
            pygame.draw.rect(self.sub_scr, 'skyblue', ((0, 20), (300 * abs(math.sin(self.f / 120 * math.pi)), 10)))  # ...和色带

    def shoot(self):
        """
        射击事件，松开R/P键时触发
        :return: 无
        """
        Bullet(self.pos.copy(), self.gun_rotate + self.base_rotate, self.base_rotate, self.v, self.num, self.left,
               self.effort, 1, self.cannot_ud, self.cannot_lr)  # 创建子弹实例
        self.f = 0  # 归零蓄力

    def hit(self, effort):
        """
        被子弹击中时的事件
        :param effort: 减少的血量
        :return: 无
        """
        self.life -= effort
        if self.life <= 0:
            game_over(self.num)  # 血量为零时结束游戏

    def lose(self):
        """
        输掉游戏时打印的文字
        :return: 无
        """
        add_text(self.sub_scr, "Game Over", (150, 80), 70, 'red')
        add_text(self.sub_scr, 'You Lose', (150, 120), 60, 'red')

    def win(self):
        """
        赢得游戏时打印的文字
        :return: 无
        """
        add_text(self.sub_scr, "Good Job!", (150, 80), 70, 'green')
        add_text(self.sub_scr, 'You Win', (150, 120), 60, 'green')


player0 = Player(sub_scr1, 0, (pygame.K_w, pygame.K_s, pygame.K_q, pygame.K_e, pygame.K_a, pygame.K_d, pygame.K_r),
                 list(random.choice(empty)))  # 实例化玩家1
player1 = Player(sub_scr2, 1, (pygame.K_i, pygame.K_k, pygame.K_u, pygame.K_o, pygame.K_j, pygame.K_l, pygame.K_p),
                 list(random.choice(empty)))  # 实例化玩家2

over = True  # 用于解除控制，当该值为True时，无法操作
loser = ...  # 失败者编号


def game_over(loser_):
    """
    游戏结束时调用的函数
    :param loser_: 失败者编号
    :return: 无
    """
    global loser, over
    loser = loser_
    if loser_ == 0:
        player0.lose()
        player1.win()
    else:
        player1.lose()
        player0.win()
    over = True
    screen.blit(sub_scr1, (0, 0))
    screen.blit(sub_scr2, (width / 2, 0))
    pygame.display.flip()


def main_update():
    """
    主更新事件
    :return: 无
    """
    global map_surf
    if not over:  # 可以控制时
        p1s, p1p = player0.main_event()  #  渲染Ⅰ阶段
        p2s, p2p = player1.main_event()
        [b.move() for b in bullets[:]]  # 子弹移动阶段
        bullet_renders = [b.render() for b in bullets]  # 渲染子弹阶段
    else:  # 不可控制时
        p1s, p1p = player0.main_display1()  # 渲染Ⅰ阶段
        p2s, p2p = player1.main_display1()
        bullet_renders = []  # 跳过子弹移动/渲染阶段
        blank_surface = pygame.Surface((100, 100))
        blank_surface.set_colorkey((0, 0, 0))
        if loser == 0:  # 将失败者的坦克移除
            p1s = blank_surface
        elif loser == 1:
            p2s = blank_surface
    # map_surf = make_map(my_map)
    player0.main_display2(p1s, p2s, p2p, bullet_renders)  # 渲染Ⅱ阶段
    player1.main_display2(p2s, p1s, p1p, bullet_renders)
    if over and loser is not ...:  # 游戏结束时……
        game_over(loser)


running = True
clock = pygame.time.Clock()
frame_before_start = 0  # 游戏正式开始前的帧数计算(用于显示文字)
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:  # 点"x" 或 按下ESC 时关闭窗口
            running = False
        if event.type == pygame.KEYUP and not over:
            if event.key == pygame.K_r:  # 开炮事件
                player0.shoot()
            elif event.key == pygame.K_p:
                player1.shoot()
            # elif event.key == pygame.K_t:
            #     game_over(0)
    # pygame.draw.line(sub_scr1, 'green', (300, 0), (300, 360), 5)
    # pygame.draw.line(sub_scr2, 'purple', (0, 0), (0, 360), 5)
    screen.fill((0, 0, 0))
    sub_scr1.fill((0, 0, 0))
    sub_scr2.fill((0, 0, 0))
    sub_scr1.blit(no_map_bg, (0, 0))  # 添加无地图时条纹背景
    sub_scr2.blit(no_map_bg, (0, 0))
    main_update()  # 进入主事件
    pygame.draw.line(sub_scr1, 'black', (300, 0), (300, 360), 2)  # 画上分割线
    pygame.draw.line(sub_scr2, 'black', (0, 0), (0, 360), 2)
    frame_before_start += 1
    if frame_before_start < 6 * 60:  # 显示文本
        text = ['Ready?', 'Ready?', '3', '2', '1', 'GO!'][frame_before_start // 60]
        color = ['red', 'red', (255, 165, 0), 'yellow', 'lightgreen', 'green'][frame_before_start // 60]
        add_text(sub_scr1, text, (300, 180), 80, color)
        add_text(sub_scr2, text, (0, 180), 80, color)
    else:
        frame_before_start = 360
    if over and frame_before_start // 60 == 5:
        over = False  # 当显示 'GO!' 时可以控制坦克(没错，文字没有消失时就可以操作了)
    screen.blit(sub_scr1, (0, 0))  # 将子屏幕渲染到主屏幕上
    screen.blit(sub_scr2, (width / 2, 0))
    pygame.display.flip()  # 更新画面

pygame.quit()
