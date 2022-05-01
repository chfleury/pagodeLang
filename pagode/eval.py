from typing import  List, Union

SExpr = Union[List, str, int]

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

