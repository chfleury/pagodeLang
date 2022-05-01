from lark import  Tree, Transformer, v_args
from typing import Dict, List, Tuple, Union

SExpr = Union[List, str, int]
FuncDef = Tuple[Tuple[str], SExpr]
IR = Dict[str, FuncDef]


def internal_representation(ast: Tree) -> IR:
    transformer = IRTransformer()
    return transformer.transform(ast)


def mk_operator(op):
    return lambda self, x, y: [op, x, y]

@v_args(inline=True)
class IRTransformer(Transformer):
    def NAME(self, tk):
        return str(tk)

    def INT(self, tk):
        y = list(filter(None, tk.value.split(' ')))

        if y[0] == 'nenhum':
            return 0
        return len(y)

    def OP(self, tk):
        return str(tk)

    def __default__(self, data, children, meta):
        raise RuntimeError(f"nó inválido: {data}")

    mul = mk_operator("*")
    add = mk_operator("+")
    sub = mk_operator("-")
    div = mk_operator("/")
    lt = mk_operator("<")
    gt = mk_operator(">")
    eq = mk_operator("=")
    bit_or = mk_operator("|")
    bit_and = mk_operator("&")

    def start(self, *funcs):
        return dict(funcs)

    def cond(self, cond, then, other):
        return ["if", cond, then, other]

    def op(self, *children):
        if len(children) == 3:
            x, op, y = children
            return [op, x, y]
        *start, op, rhs = children
        return [op, self.op(*start), rhs]

    def call(self, name, args):
        return [name, *args]

    def args(self, *args):
        return args

    def argn(self, *args):
        return [str(x) for x in args]

    def func(self, name, args, body):
        return str(name), (args, body)
