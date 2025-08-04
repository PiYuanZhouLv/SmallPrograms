import random
from matplotlib import pyplot as plt
import numpy as np
from rich import progress

def simulate(n=100, movement=((-1, 0.6), (1, 0.2), (2, 0.2)), start_at=-1, target_at=0, low_boundry=-3000, high_boundry=3000, life_limit=10000, absorb_prob=1, _pg=None):
    movement_count = {k: 0 for k, _ in movement}
    end_case = {
        'hit': 0,
        'esc': 0,
        'die': 0
    }
    if start_at == target_at and absorb_prob >= 1:
        return movement_count, end_case|{'hit': n}
    moves, weights = tuple(zip(*movement))
    if not _pg:
        pg = progress.Progress()
        pg.__enter__()
        need_exit = True
    else:
        pg = _pg
        need_exit = False
    try:
        tsk = pg.add_task('simulating...', total=n)
        for _ in range(n):
            pos = start_at
            if pos == target_at and random.random() <= absorb_prob:
                end_case['hit'] += 1
                continue
            for _ in range(life_limit):
                move = random.choices(moves, weights)[0]
                movement_count[move] += 1
                pos += move
                if pos == target_at and random.random() <= absorb_prob:
                    end_case['hit'] += 1
                    break
                elif pos <= low_boundry or pos >= high_boundry:
                    end_case['esc'] += 1
                    break
            else:
                end_case['die'] += 1
            pg.advance(tsk)
        pg.remove_task(tsk)
    finally:
        if need_exit:
            pg.__exit__()
    return {k: v/sum(movement_count.values()) for k, v in movement_count.items()}, end_case

def plot(movement, range_from=-100, range_to=100, n=100, lx=None, ly=None, lc='red', show=True, **kwargs):
    yh = []
    ye = []
    yd = []
    x = []
    with progress.Progress() as pg:
        tsk = pg.add_task('calcing...', total=range_to-range_from+1)
        for i in range(range_from, range_to+1):
            x.append(i)
            result = simulate(n, movement, i, **kwargs, _pg=pg)[1]
            yh.append(result['hit']/n)
            ye.append(result['esc']/n)
            yd.append(result['die']/n)
            pg.advance(tsk)
    x, yh, ye, yd = tuple(map(np.array, (x, yh, ye, yd)))
    plt.bar(x, yh, align='center', label='hit')
    plt.bar(x, ye, bottom=yh, color='orange', alpha=0.3, label='esc')
    plt.bar(x, yd, bottom=yh+ye, color='yellow', alpha=0.3, label='die')
    plt.legend()
    if lx is not None and ly is not None:
        if isinstance(ly, (tuple, list)):
            for i, liney in enumerate(ly):
                linex = lx[i] if isinstance(lx, (tuple, list)) else lx
                linec = lc[i] if isinstance(lc, (tuple, list)) else lc
                plt.plot(linex, liney, c=linec)
        else:
            plt.plot(lx, ly, c=lc)
    if show:
        plt.show()
    return yh, ye, yd

if __name__ == '__main__':
    import code
    code.interact(local=globals())