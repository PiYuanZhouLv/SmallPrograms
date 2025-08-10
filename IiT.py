import time
st = time.time()

import colorsys
import glob
import os
import random
import sys

import numpy as np
import rich.console
from PIL import Image

chr_l = {'a': 0.4480769230769231, 'b': 0.4980769230769231, 'c': 0.3057692307692308, 'd': 0.5019230769230769, 'e': 0.4230769230769231, 'f': 0.3173076923076923, 'g': 0.5442307692307692, 'h': 0.4269230769230769, 'i': 0.18076923076923077, 'j': 0.25961538461538464, 'k': 0.4115384615384615, 'l': 0.22884615384615384, 'm': 0.5461538461538461, 'n': 0.36346153846153845, 'o': 0.38076923076923075, 'p': 0.475, 'q': 0.47692307692307695, 'r': 0.23076923076923078, 's': 0.3423076923076923, 't': 0.2903846153846154, 'u': 0.3903846153846154, 'v': 0.3076923076923077, 'w': 0.5711538461538461, 'x': 0.34615384615384615, 'y': 0.38461538461538464, 'z': 0.35, 'A': 0.5557692307692308, 'B': 0.698076923076923, 'C': 0.4634615384615385, 'D': 0.6288461538461538, 'E': 0.5346153846153846, 'F': 0.42115384615384616, 'G': 0.6403846153846153, 'H': 0.5307692307692308, 'I': 0.27307692307692305, 'J': 0.29615384615384616, 'K': 0.5269230769230769, 'L': 0.36923076923076925, 'M': 0.8288461538461539, 'N': 0.6788461538461539, 'O': 0.5980769230769231, 'P': 0.4846153846153846, 'Q': 0.698076923076923, 'R': 0.5961538461538461, 'S': 0.5134615384615384, 'T': 0.3269230769230769, 'U': 0.6, 'V': 0.4673076923076923, 'W': 0.8730769230769231, 'X': 0.5442307692307692, 'Y': 0.3576923076923077, 'Z': 0.5346153846153846, '/': 0.22115384615384615, '<': 0.25, '>': 0.23461538461538461, '?': 0.33076923076923076, ';': 0.1, ':': 0.08076923076923077, '[': 0.3230769230769231, ']': 0.3230769230769231, '{': 0.29615384615384616, '}': 0.29615384615384616, '\\': 0.225, '|': 0.2076923076923077, '1': 0.3096153846153846, '2': 0.475, '3': 0.5, '4': 0.46153846153846156, '5': 0.5326923076923077, '6': 0.5038461538461538, '7': 0.3769230769230769, '8': 0.5923076923076923, '9': 0.5211538461538462, '0': 0.49423076923076925, '!': 0.20384615384615384, '@': 1.0, '#': 0.6653846153846154, '$': 0.698076923076923, '%': 0.7788461538461539, '&': 0.676923076923077, '*': 0.21923076923076923, '(': 0.3153846153846154, ')': 0.3192307692307692, '+': 0.27115384615384613, '`': 0.0673076923076923, '~': 0.14807692307692308, ' ': 0.0}
name_l, value_l = list(zip(*sorted(list(chr_l.items()), key=lambda x: x[1])))
value_l = np.array(value_l)


def get_ascii(l):
    if '--darker' in sys.argv:
        l = l * (1 - 0.1*min(sys.argv.count('--darker'), 9))
    return name_l[np.argmin(np.abs(value_l - l))].replace('\\', '\\\\')


con = rich.console.Console()
con_width = ((con.width - 1 if con.width <= 200 or '--slow' in sys.argv else con.width - 5)
             if '-w' not in sys.argv else int(sys.argv[sys.argv.index('-w') + 1]))

if ((con.color_system != 'truecolor' and '--ignore' not in sys.argv)
        and ('--ascii-art' not in sys.argv and '--nocolor' not in sys.argv)):
    rich.print('[blink red on yellow bold]:warning:Warning!:warning:[/]')
    rich.print("[red]Your Terminal doesn't support truecolor[/]")
    rich.print(f"You color system is: {con.color_system}")
    rich.print("💡hits1: pass '--ignore' to ignore this message")
    rich.print("💡hits2: pass '--ascii-art --nocolor' to use in the hard situation")
    sys.exit(1)
elif con.color_system is None and ('--ascii-art' not in sys.argv and '--nocolor' not in sys.argv):
    rich.print("[bold underline]Do not try anymore.")
    rich.print("Your Terminal does NOT support ANY color.")
    rich.print("But don't worry about it, pass '--ascii-art --nocolor' to use in such a hard situation :)")
    sys.exit(1)

ch = '▄' if '--half' not in sys.argv else ' '
ch_width = con.measure(ch).maximum

pixel_width = con_width // ch_width

if os.path.exists('last.IiT'):
    with open('last.IiT') as f:
        os.environ['IiTLastOpen'] = f.read().strip()

if len(sys.argv) > 1:
    if sys.argv[1] == 'demo':
        img = Image.open(r'D:\温予乐\我的桌面\sl\IiT\3.jpg').convert('RGB')
        os.environ['IiTLastOpen'] = ''
    elif sys.argv[1] == 'random':
        exp = ['.png', '.jpg', '.jpeg', '.bmp', '.jfif', '.gif', '.webp']
        fl = []
        for e in exp:
            fl += glob.glob(f'*{e}')
        file = random.choice(fl)
        sys.argv[1] = file
        img = Image.open(file).convert('RGB')
        os.environ['IiTLastOpen'] = os.path.abspath(file)
    elif sys.argv[1] == 'last':
        file = os.environ.get('IiTLastOpen', '')
        if not file:
            img = Image.open(r'D:\温予乐\我的桌面\sl\IiT\3.jpg').convert('RGB')
        else:
            sys.argv[1] = file
            img = Image.open(file).convert('RGB')
    else:
        img = Image.open(sys.argv[1]).convert('RGB')
        os.environ['IiTLastOpen'] = os.path.abspath(sys.argv[1])
else:
    img = Image.open(r'D:\温予乐\我的桌面\sl\IiT\3.jpg').convert('RGB')
    os.environ['IiTLastOpen'] = ''
# img.save('tmp.png')
if "--line" in sys.argv:
    a = np.asarray(img.convert('L')).astype('float')

    # 根据灰度变化来模拟人类视觉的明暗程度
    depth = 10.  # 预设虚拟深度值为10 范围为0-100
    grad = np.gradient(a)  # 提取梯度值
    grad_x, grad_y = grad  # 提取x y方向梯度值 解构赋给grad_x, grad_y

    # 利用像素之间的梯度值和虚拟深度值对图像进行重构
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.  # 根据深度调整x y方向梯度值

    # 梯度归一化 定义z深度为1.  将三个梯度绝对值转化为相对值，在三维中是相对于斜对角线A的值
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    # 令三维中是相对于斜对角线的值为1
    vec_el = np.pi / 2.1  # 光源俯视角度   弧度值  接近90度
    vec_az = np.pi / 4.  # 光源方位角度   弧度值  45度
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x轴的影响 对角线在x轴投影
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y轴的影响 对角线在y轴投影
    dz = np.sin(vec_el)  # 光源对z轴的影响 对角线在z轴投影

    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    b = b.clip(0, 255)  # 为了避免数据越界，生成灰度值限制在0-255区间
    b = (1 - b / 255)
    p = np.percentile(b, 85)
    if "--nocolor" in sys.argv:
        b = (b > p) * 255 if "--reverse" not in sys.argv else (b < p) * 255
    elif "--green" not in sys.argv:
        b = np.array(img)*np.append(b[:, :, np.newaxis],
                                    np.append(b[:, :, np.newaxis], b[:, :, np.newaxis], axis=2), axis=2).clip(100/255, 1)
    else:
        s = b > p
        sb = np.append(s[:, :, np.newaxis],
                       np.append(s[:, :, np.newaxis], s[:, :, np.newaxis], axis=2), axis=2)
        s = sb * [0, 1e10, 0] + (1 - sb) * [1, 1, 1]
        b = (np.array(img) * s).clip((0, 0, 0), (255, 255, 255))
    img = Image.fromarray(b.astype('uint8')).convert("RGB")  # 图像更构
    if "--save-tmp" in sys.argv:
        img.save(sys.argv[sys.argv.index("--save-tmp")+1])

if '-r' in sys.argv:
    img = img.rotate(270, expand=True)
W, H = img.size
S = (0.9 if con_width <= 900 else (0.8 if con_width <= 1800 else 0.7)) if '-s' not in sys.argv else float(
    sys.argv[sys.argv.index('-s') + 1])
img = img.resize(size=(
    pixel_width,
    int(pixel_width / W * H * S)
))

img_list = np.array(img).tolist()

if '--record' in sys.argv:
    con.record = True

try:
    ls = []
    for lineno in range(0, len(img_list), 2):
        line_output = []
        if lineno + 1 != len(img_list):
            for cell, cell2 in zip(img_list[lineno], img_list[lineno + 1]):
                if '--ascii-art' in sys.argv:
                    ch = get_ascii((cell[0] * 0.299 + cell[1] * 0.587 + cell[2] * 0.114) / 256)
                    if '--nocolor' in sys.argv:
                        cell = cell2 = [255, 255, 255]
                if "--slow" not in sys.argv:
                    line_output.append(f'[#{cell2[0]:0>2X}{cell2[1]:0>2X}{cell2[2]:0>2X} '
                                       f'on #{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X}]{ch}[/]'
                                       if '--ascii-art' not in sys.argv else
                                       f"[#{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X} on black]{ch}[/]")
                else:
                    con.print(f'[#{cell2[0]:0>2X}{cell2[1]:0>2X}{cell2[2]:0>2X} '
                              f'on #{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X}]{ch}[/]'
                              if '--ascii-art' not in sys.argv else
                              f"[#{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X} on black]{ch}[/]", end='')
        else:
            for i, cell in enumerate(img_list[lineno]):
                if '--ascii-art' in sys.argv:
                    ch = get_ascii((cell[0] * 0.299 + cell[1] * 0.587 + cell[2] * 0.114) / 256)
                    if "--nocolor" in sys.argv:
                        cell = [255, 255, 255]
                h = i / pixel_width
                cell2 = colorsys.hls_to_rgb(h, 0.5, 1)
                cell2 = [int(c * 255) for c in cell2]
                if "--slow" not in sys.argv:
                    line_output.append(f'[#{cell2[0]:0>2X}{cell2[1]:0>2X}{cell2[2]:0>2X} '
                                       f'on #{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X}]{ch}[/]'
                                       if '--ascii-art' not in sys.argv else
                                       f"[#{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X} on black]{ch}[/]")
                else:
                    con.print(f'[#{cell2[0]:0>2X}{cell2[1]:0>2X}{cell2[2]:0>2X} '
                              f'on #{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X}]{ch}[/]'
                              if '--ascii-art' not in sys.argv else
                              f"[#{cell[0]:0>2X}{cell[1]:0>2X}{cell[2]:0>2X} on black]{ch}[/]", end='')
        # con.print(''.join(line_output), end='\n')
        ls.append(''.join(line_output))
        if lineno % 1 == 0:
            con.print('\n'.join(ls))
            ls = []
except KeyboardInterrupt:
    con.print('[red on #FFFF00 bold]Aborted[/]')

con.print('\n'.join(ls))
con.print(f'{"demo pic" if len(sys.argv) == 1 else sys.argv[1]}')
con.print(f'{W}x{H}(scale to {pixel_width}x{int(pixel_width / W * H * S)})')
et = time.time()
con.print(f'Spend {et-st:.2f}s')
if '--record' in sys.argv:
    try:
        con.save_html(sys.argv[sys.argv.index('--record') + 1])
    except IndexError:
        con.save_html(f'./save.html')

with open('last.IiT', 'w') as f:
    f.write(os.environ['IiTLastOpen'])
