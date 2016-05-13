from .base import Base

class Expression(Base):

    commutative = True

    def __new__(cls, *terms, **kwargs):

        from .order import canonical_order
        from .common import convert_type

        if 'simplify' in kwargs:
            simp = kwargs['simplify']
        else:
            simp = True

        args = list(map(convert_type, terms))

        if simp:
            args = cls.simplify(args)

            if len(args) == 1:
                return args[0]

            if cls.commutative:
                args.sort(key=canonical_order)

        obj = super(Expression, cls).__new__(cls)
        obj.args = args

        return obj

    @classmethod
    def simplify(cls, seq):
        """ Simplifies args of the expression, in respect to that expression. Should be overidden for majority of cases.

        This method is called during the __new__ stage of the creation of a Expression subclass (but not if
        simplify=False is passed in the constructor).
        This enables simplification to occur *before* the creation of the class that was specified.
        This is important as simplification can result in transformation of the root node, i.e:

        x + x -> 2x, Add(x, x) -> Mul(2, x)

        Args:
            cls: The class simplify is being called from (automatically fulfilled)
            seq: The args of the Expression

        Returns:
            list of simplified args

        """

        # In case child class does not need to implement simplification leave the args untouched
        return seq
    
    def __add__(self, other):
        return super(Expression, self).__add__(other)
    
    def __mul__(self, other):
        return super(Expression, self).__mul__(other)
    
    def __pow__(self, power, modulo=None):
        return super(Expression, self).__pow__(power)
    
    def __lt__(self, other):
        return super(Expression, self).__lt__(other)
    
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.args == other.args
        else:
            return super(Expression, self).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.args))

    def __repr__(self):
        return self.__class__.__name__ + str(self.args)