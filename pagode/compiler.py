from lark import Lark, Tree
from pathlib import Path
from typing import Dict, List, Tuple, Union
import operator as op
from .ir import internal_representation

AST = Tree
SExpr = Union[List, str, int]

GRAMMAR_PATH = Path(__file__).parent / "grammar.lark"
GRAMMAR_SRC = GRAMMAR_PATH.read_text()
GRAMMAR = Lark(GRAMMAR_SRC)
GLOBAL_ENV = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.truediv,
    "<": lambda x, y: int(x < y),
    ">": lambda x, y: int(x > y),
    "=": lambda x, y: int(x == y),
    "|": op.or_,
    "&": op.and_,
}


def pagode(src: str, env: dict):
    ast = parse(src)
    ir = internal_representation(ast)
    interpret(ir, env)


def interpret(ir, env):
    # Interpretação do código
    env.update(GLOBAL_ENV)

    main_args = None
    for fname, (args, body) in ir.items():
        if fname == "Ela":
            main_args = [int(input("argumento: ")) for arg in args]
        env[fname] = make_function(args, body, env)

    print("\n=>", env["Ela"](*main_args))


def parse(src: str) -> AST:
    return GRAMMAR.parse(src)




def eval_expr(sexpr: SExpr, env: dict):
    if isinstance(sexpr, int):
        return sexpr
    elif isinstance(sexpr, str):
        return env[sexpr]

    head, *args = sexpr
    if head == "if":
        cond, then, other = args
        if eval_expr(cond, env):
            return eval_expr(then, env)
        else:
            return eval_expr(other, env)

    fn = env[head]
    argvalues = [eval_expr(arg, env) for arg in args]
    return fn(*argvalues)


def make_function(argnames, body, env):
    def fn(*argvalues):
        local_env = env.copy()
        for name, value in zip(argnames, argvalues):
            local_env[name] = value
        return eval_expr(body, local_env)

    return fn



