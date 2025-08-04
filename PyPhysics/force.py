import numpy as np
import pygame
import colorsys
import random
import math
from typing import Literal

def random_color(light):
    rgb = colorsys.hls_to_rgb(random.random(), light, random.random()*0.5+0.5)
    return tuple(map(lambda x: int(x*256), rgb))

def rad_to_vec(dir):
    return np.array([math.cos(dir), math.sin(dir)])

def vec_to_rad(arr):
    arr = arr.copy()
    arr /= (arr**2).sum()**0.5
    return math.acos(arr[0]) if arr[1] >= 0 else 2 * math.pi - math.acos(arr[0])

def arr_to_pos(arr):
    return list(map(int, arr.tolist()))

def draw_arrow(surface: pygame.Surface, sp, dir, length, width, color):
    ep = sp + rad_to_vec(dir) * length
    pygame.draw.line(surface, color, arr_to_pos(sp), arr_to_pos(ep), width)
    p1 = sp + rad_to_vec(dir) * (length - 5 * width) + rad_to_vec(dir - math.pi / 2) * 5 * width
    p2 = sp + rad_to_vec(dir) * (length - 5 * width) + rad_to_vec(dir + math.pi / 2) * 5 * width
    pygame.draw.lines(surface, color, False, list(map(arr_to_pos, [p1, ep, p2])), width)

def draw_text(surface: pygame.Surface, text, color, pos, fontsize):
    sur = pygame.font.SysFont('LXGW Wenkai', fontsize).render(text, True, color)
    rect = sur.get_rect()
    rect.center = pos
    surface.blit(sur, rect)

class FixedPoint:
    def __init__(self, x, y, m=0) -> None:
        self.pos = np.array([x, y], 'float64')
        self.mass = m
        self.color = 'red'
    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, arr_to_pos(self.pos), 5)
    def force(self, f):
        pass
    def tick(self, dt):
        pass
    def clear_force(self):
        pass

class MassPoint:
    def __init__(self, x, y, m, v=None):
        self.pos = np.array([x, y], 'float64')
        self.mass = m
        self.velc = v if v is not None else np.array([0, 0], 'float64')
        self.color = random_color(0.8)
        self._force = np.zeros(2)
    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, arr_to_pos(self.pos), 5)
    def force(self, force):
        self._force += force
    def tick(self, dt):
        self.velc += self._force / self.mass * dt
        self.pos += self.velc * dt
    def clear_force(self):
        self._force = np.zeros(2)

class ConstantForce:
    def __init__(self, obj, dir, f):
        self.obj = obj
        self.f = rad_to_vec(dir) * f
    def tick(self):
        self.obj.force(self.f)

class HotMovementForce:
    def __init__(self, *objs, mean, var) -> None:
        self.objs = objs
        self.mean = mean
        self.var = var
    def tick(self):
        for obj in self.objs:
            obj.force(rad_to_vec(random.random()*2*math.pi)*random.gauss(self.mean, self.var))

class ElasticForce:
    def __init__(self, obj1, obj2, k, l0 = 0, reversible = True) -> None:
        self.obj1 = obj1
        self.obj2 = obj2
        self.k = k
        self.l0 = l0
        self.reversible = reversible
    def tick(self):
        f = (((self.obj1.pos - self.obj2.pos)**2).sum()**0.5 - self.l0) * self.k
        if not self.reversible:
            f = f if f > 0 else 0
        fv = (self.obj1.pos - self.obj2.pos) / (((self.obj1.pos - self.obj2.pos)**2).sum()**0.5+1e-100) * f
        self.obj2.force(fv)
        self.obj1.force(-fv)

class UniversalGravitation:
    def __init__(self, *objs, G, limit = 10) -> None:
        self.objs = list(objs)
        self.G = G
        self.limit = limit
    def tick(self):
        objs = self.objs[:]
        while objs:
            obj1 = objs.pop()
            for obj2 in objs:
                if ((obj1.pos - obj2.pos)**2).sum() <= self.limit:
                    continue
                f = obj1.mass * obj2.mass / ((obj1.pos - obj2.pos)**2).sum() * self.G * ((obj1.pos - obj2.pos) / ((obj1.pos - obj2.pos)**2).sum()**0.5)
                obj2.force(f)
                obj1.force(-f)

sqrt = lambda x: x ** 0.5

# 注：当初不知道粒子相互作用力表达式，
# 实际上好像是 F = - A/r^2 + Be^(-rC) ?
# 算了，懒得改。
class ElectionLikeForce:
    def __init__(self, *objs, s, p, q, k=1) -> None:
        self.objs = list(objs)
        self.a = p**2*q*(p**2 - 3*s**2 - sqrt(p**4 - 6*p**2*s**2 + 8*p*s**3 - 3*s**4))/(2*s*(2*p - 3*s))
        self.b = p**2*q*(-2*p**5 + 3*p**4*s + 6*p**3*s**2 - 2*p**3*sqrt(p**4 - 6*p**2*s**2 + 8*p*s**3 - 3*s**4) - 16*p**2*s**3 + 3*p**2*s*sqrt(p**4 - 6*p**2*s**2 + 8*p*s**3 - 3*s**4) + 12*p*s**4 - 3*s**5 - s**3*sqrt(p**4 - 6*p**2*s**2 + 8*p*s**3 - 3*s**4))/(2*s**4*(2*p - 3*s))
        self.c = p*(-p**2 + 3*s**2 - sqrt(p**4 - 6*p**2*s**2 + 8*p*s**3 - 3*s**4))/(2*s**2)
        if self.c < 0:
            print('Warning! ElectionLikeForce\'s c-value is minus, which could lead to strange phenomena.')
        self.k = k
    def tick(self):
        objs = self.objs[:]
        while objs:
            obj1 = objs.pop()
            for obj2 in objs:
                d = ((obj1.pos - obj2.pos)**2).sum()**0.5
                f = self.a / d ** 2 - self.b / (d - self.c) ** 2
                fv = self.k * f * ((obj1.pos - obj2.pos) / ((obj1.pos - obj2.pos)**2).sum()**0.5)
                obj2.force(fv)
                obj1.force(-fv)
    @staticmethod
    def helper(sp=0, ep=1000, dp=1, ss=0, es=1000, ds=1):
        import numpy as np
        import matplotlib.pyplot as plt
        p = np.arange(sp, ep, dp)
        s = np.arange(ss, es, ds)
        p, s = np.meshgrid(p, s)
        c = p*(-p**2 + 3*s**2 - sqrt(p**4 - 6*p**2*s**2 + 8*p*s**3 - 3*s**4))/(2*s**2)
        plt.imshow(c>0)
        plt.show()

class FakeMeasurePoint:
    def __init__(self, x, y) -> None:
        self.pos = np.array([x, y], 'float64')
        self.velc = np.array([0, 0], 'float64')

class DistanceMeasure:
    def __init__(self, obj1, obj2, show: Literal['real', 'diff', 'line']='real') -> None:
        self.obj1 = obj1
        self.obj2 = obj2
        self.last_dist = 0
        self.show = show
    def render(self, sur: pygame.Surface):
        d = ((self.obj1.pos - self.obj2.pos)**2).sum()**0.5
        ds = f'{d-(0 if self.show != "diff" else self.last_dist):{"+" if self.show == "diff" else ""}.2f}'
        pygame.draw.line(sur, (255, 0, 0) if d - self.last_dist < 0 else (0, 255, 0), arr_to_pos(self.obj1.pos), arr_to_pos(self.obj2.pos))
        if self.show != 'line':
            draw_text(sur, ds, (255, 0, 0) if d - self.last_dist < 0 else (0, 255, 0), arr_to_pos((self.obj1.pos + self.obj2.pos)/2), 20)
        self.last_dist = d

class VelocityMeasure:
    def __init__(self, obj, ref = None, scale = 1, show:Literal['real', 'diff', 'line'] = 'real') -> None:
        self.obj = obj
        self.ref = ref or FakeMeasurePoint(0, 0)
        self.last_velc = 0
        self.show = show
        self.scale = scale
    def render(self, surface):
        velc = self.obj.velc - self.ref.velc
        vv = (velc**2).sum()**0.5
        color = (0, 255, 0) if vv > self.last_velc else (255, 0, 0)
        draw_arrow(surface, self.obj.pos, vec_to_rad(velc), vv*self.scale, 2, color)
        if self.show != 'line':
            draw_text(surface, f'{"Δv=" if self.show=="diff" else "v="}{vv-(0 if self.show!="diff" else self.last_velc):{"+" if self.show=="diff" else ""}.2f}', color, self.obj.pos+velc*(self.scale+10/vv), 20)
        self.last_velc = vv

class TraceMeasure:
    def __init__(self, obj, skip=49, maximun=100) -> None:
        self.obj = obj
        self.skip = skip
        self.count = 0
        self.pos_record = []
        self.maximun = maximun
        self.color = obj.__dict__.get('color', random_color(0.5))
    def render(self, sur: pygame.Surface):
        self.count -= 1
        if self.count < 0:
            self.pos_record.append(arr_to_pos(self.obj.pos))
            self.count = self.skip
        if len(self.pos_record) > self.maximun:
            self.pos_record.pop(0)
        pygame.draw.lines(sur, self.color, False, self.pos_record+[arr_to_pos(self.obj.pos)])

def simulate(objs, forces, measures=[], fps=0, slow_rate=1, video=None):
    pygame.init()
    if not video:
        screen = pygame.display.set_mode((600, 600))
        dx, dy = 0, 0
        scale = 1
        paused = False
        clock = pygame.time.Clock()
    if video:
        from rich import progress
        import time
        import os
        pg = progress.Progress()
        fps = video.get('fps', fps) or 60
        skp_setting = video.get('skp', 20)
        total = int(video.get('length', 5) * fps)
        cf0 = 0
        skp = skp_setting
        tsk = pg.add_task('正在生成……', total=total)
        pg.__enter__()
        path = time.strftime('%Y-%m-%d %H.%M.%S', time.localtime())
        os.mkdir(path)
    while not video or total:
        if not video:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # TODO: Scale & Move
        if video:
            skp -= 1
        for force in forces:
            force.tick()
        for obj in objs:
            obj.tick(1 / (fps or clock.get_fps() or 200) / slow_rate if not video else 1 / fps / skp_setting)
            obj.clear_force()
        if not video or not skp:
            sur = pygame.Surface((600, 600))
            for measure in measures:
                measure.render(sur)
            for obj in objs:
                obj.render(sur)
        if not video:
            screen.fill((0, 0, 0))
            sur = pygame.transform.scale_by(sur, scale)
            screen.blit(sur, sur.get_rect().move(dx, dy))
            screen.blit(pygame.font.SysFont('LXGW Wenkai', 30).render(f'FPS: {clock.get_fps():.2f}', True, (255, 255, 255)), (0, 0))
            pygame.display.flip()
        if video and not skp:
            total -= 1
            cf0 += 1
            skp = skp_setting
            pygame.image.save(sur, os.path.join(path, f'{cf0}.png'))
            pg.advance(tsk)
    if video:
        pg.__exit__(None, None, None)
        os.system(f'ffmpeg -r {fps} -i "{os.path.join(path, "%d.png")}" "{path}.mp4"')
        import shutil
        shutil.rmtree(path)


if __name__ == '__main__':
    def hmv_with_g():
        balls = []
        trace = []
        for i in range(10):
            ball = MassPoint(300, 300, .5)
            balls.append(ball)
            trace.append(TraceMeasure(ball, 29))
        f = HotMovementForce(*balls, mean=1, var=5)
        g = UniversalGravitation(*balls, G=1, limit=1)
        simulate(balls, [f, g], trace)
    
    def hmv():
        balls = []
        trace = []
        for i in range(10):
            ball = MassPoint(300, 300, .5)
            balls.append(ball)
            trace.append(TraceMeasure(ball, 29))
        f = HotMovementForce(*balls, mean=20, var=5)
        simulate(balls, [f], trace)
    
    def two_mp():
        p1 = MassPoint(150, 300, 1)
        p2 = MassPoint(450, 300, 1)
        f = ElasticForce(p1, p2, 10)
        simulate([p1, p2], [f])
    
    def two_circle():
        m1 = 5
        m2 = 10
        d = 300
        omega = 0.3

        d1 = m2 / (m1 + m2) * d
        d2 = m1 / (m1 + m2) * d
        G = d ** 2 / m2 * d1 * omega
        p1 = MassPoint(300-d1, 300, m1, np.array([0, -d1*omega], 'float64'))
        p2 = MassPoint(300+d2, 300, m2, np.array([0, d2*omega], 'float64'))
        f = UniversalGravitation(p1, p2, G=G)
        dm1 = DistanceMeasure(p1, FakeMeasurePoint(300, 300), 'real')
        dm2 = DistanceMeasure(p2, FakeMeasurePoint(300, 300), 'real')
        tm1 = TraceMeasure(p1, 29, 40)
        tm2 = TraceMeasure(p2, 29, 40)
        simulate([p1, p2], [f], [dm1, dm2, tm1, tm2])
    
    def one_round_one():
        mc = 5
        mp = 5
        d = 150
        v = 100
        vpv0 = 0.7

        v0 = v / vpv0
        G = v0 ** 2 * d / mc
        planet = MassPoint(300-d, 300, mp, np.array([0, -v], 'float64'))
        center = FixedPoint(300, 300, mc)
        g = UniversalGravitation(planet, center, G=G)
        dm = DistanceMeasure(planet, center, 'real')
        tm = TraceMeasure(planet)
        vm = VelocityMeasure(planet, scale=0.1, show='real')
        simulate([planet, center], [g], [dm, tm, vm])

    def shm():
        m = 1
        k = 1
        v0 = 100

        point = MassPoint(300, 300, m, np.array([v0, 0], 'float64'))
        f = ElasticForce(point, FixedPoint(300, 300), k)
        vm = VelocityMeasure(point)
        dm = DistanceMeasure(point, FakeMeasurePoint(300, 300))
        simulate([point], [f], [vm, dm])
    
    def elctornic_like_force_expriment():
        MEASURE = True

        balls = []
        forces = []
        measures = []
        for i in range(13):
            b1 = MassPoint(300-(80+120/12*i), 100+400/12*i, 1)
            print(80+120/12*i)
            b2 = MassPoint(300+(80+120/12*i), 100+400/12*i, 1)
            forces.append(ElectionLikeForce(b1, b2, s=200, p=250, q=1000))
            balls.append(b1)
            balls.append(b2)
            measures.append(VelocityMeasure(b1))
            measures.append(DistanceMeasure(b2, FakeMeasurePoint(300, 100+400/12*i)))
        simulate(balls, forces, measures if MEASURE else [], slow_rate=10)
    
    def elctornic_expriment():
        N = 20

        balls = []
        trace = []
        for i in range(N):
            ball = MassPoint(random.random()*600, random.random()*600, 1)
            balls.append(ball)
            trace.append(TraceMeasure(ball, 29))
        elf = ElectionLikeForce(*balls, s=10, p=12, q=20)
        simulate(balls, [elf], trace)
    
    def elctornic_expriment2():
        N = 50
        r = 150
        v = 20
        q = 20

        balls = []
        trace = []
        for i in range(N):
            pos = rad_to_vec(i * 2 * math.pi / N) * r + np.array([300, 300], 'float64')
            ball = MassPoint(pos[0], pos[1], 1, rad_to_vec(i * 2 * math.pi / N + math.pi / 2) * v)
            if i == 0:
                ball.color = 'red'
            balls.append(ball)
            trace.append(TraceMeasure(ball, 0, 180))
        elf = ElectionLikeForce(*balls, s=10, p=12, q=q)
        simulate(balls, [elf], trace, video={'length': 20})
    
    elctornic_expriment2()
