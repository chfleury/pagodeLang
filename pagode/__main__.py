from pprint import pprint
import click
from .compiler import pagode, parse, internal_representation


@click.command("pagode")
@click.argument("file", type=click.File())
@click.option("--debug", "-d", is_flag=True, help="Run pagode in debug mode")
def main(file, debug):
    """
    Read and run the given pagode file.
    """
    src = file.read()
    if debug:
        ast = parse(src)
        print(ast.pretty())
        ir = internal_representation(ast)
        pprint(ir)
    else:
        pagode(src, {})

if __name__ == "__main__":
    main()
