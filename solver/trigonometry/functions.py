from solver.core.function import Function

class sin(Function):

    name = 'sin'

    def __init__(self, x):
        super(sin, self).__init__(x)


class cos(Function):

    name = 'cos'

    def __init__(self, x):
        super(cos, self).__init__(x)


class tan(Function):

    name = 'tan'

    def __init__(self, x):
        super(tan, self).__init__(x)


class asin(Function):

    name = 'asin'

    def __init__(self, x):
        super(asin, self).__init__(x)


class acos(Function):

    name = 'acos'

    def __init__(self, x):
        super(acos, self).__init__(x)


class atan(Function):

    name = 'atan'

    def __init__(self, x):
        super(atan, self).__init__(x)


class cosec(Function):

    name = 'cosec'

    def __init__(self, x):
        super(cosec, self).__init__(x)


class sec(Function):

    name = 'sec'

    def __init__(self, x):
        super(sec, self).__init__(x)


class cot(Function):

    name = 'cot'

    def __init__(self, x):
        super(cot, self).__init__(x)
