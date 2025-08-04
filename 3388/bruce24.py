import math


def bruce24(arg):
    def choose(arg):
        out = []
        for i in range(len(arg)):
            if arg[i]not in out:
                out.append(arg[i])
                yield arg[i], arg[:i]+arg[i+1:]
    def calc(program):
        program = list(program)
        stack = []
        while program:
            inst = program.pop(0)
            if isinstance(inst, int):
                stack.append(inst)
            elif inst == '+':
                stack.append(stack.pop(-2)+stack.pop())
            elif inst == '-':
                stack.append(stack.pop(-2)-stack.pop())
            elif inst == '*':
                stack.append(stack.pop(-2)*stack.pop())
            elif inst == '/':
                stack.append(stack.pop(-2)/(stack.pop()+1e-10))
        return stack.pop()
    def bruce(arg, n=0):
        if len(arg) == 0 and n == 1:
            yield []
        elif n < 2:
            for chosen, left in choose(arg):
                for prog in bruce(left, n+1):
                    yield [chosen] + prog
        elif len(arg) == 0 and n > 1:
            for op in '+-*/':
                for prog in bruce(arg, n-1):
                    yield [op] + prog
        else:
            for chosen, left in choose(arg):
                for prog in bruce(left, n+1):
                    yield [chosen] + prog
            for op in '+-*/':
                for prog in bruce(arg, n-1):
                    yield [op] + prog
    def render(program):
        program = list(program)
        stack = []
        while program:
            inst = program.pop(0)
            if isinstance(inst, int):
                stack.append(inst)
            elif inst == '+':
                stack.append(f'({stack.pop(-2)}+{stack.pop()})')
            elif inst == '-':
                stack.append(f'({stack.pop(-2)}-{stack.pop()})')
            elif inst == '*':
                stack.append(f'({stack.pop(-2)}*{stack.pop()})')
            elif inst == '/':
                stack.append(f'({stack.pop(-2)}/{stack.pop()})')
        return stack.pop()[1:-1]
    for program in bruce(arg):
        if math.isclose(24, calc(program)):
            print(render(program))

if __name__ == '__main__':
    bruce24([3, 3, 8, 8])