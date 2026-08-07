import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
async def _():
    # Get the current notebook URL, drop the 'blob' URL components that seem to be added,
    # and add the buildnumber that a makethedocs PR build seems to add. This allows to load
    # the wheel both locally and when deployed to makethedocs.
    async def import_xdsl():
        import re
        from urllib.parse import urlparse

        import micropip
        from marimo import notebook_location

        url = str(notebook_location()).replace("blob:", "")
        print(f"DEBUG: notebook url (full): {url}")

        url_parsed = urlparse(url)
        scheme = url_parsed.scheme
        netloc = url_parsed.netloc

        print(f"DEBUG: notebook url (parsed): {url_parsed}")

        url = re.sub(
            "([^/])/([a-f0-9-]+-[a-f0-9-]+-[a-f0-9-]+-[a-f0-9-]+)", "\\1/", url, count=1
        )
        buildnumber = re.sub(".*--([0-9+]+).*", "\\1", url, count=1)

        new_url = scheme + "://" + netloc

        if buildnumber != url:
            new_url = new_url + "/" + buildnumber + "/"

        print(f"DEBUG: notebook url (trimmed): {new_url}")

        await micropip.install("xdsl @ " + new_url + "/xdsl-0.0.0-py3-none-any.whl")

    await import_xdsl()
    from xdsl.utils import marimo as xmo

    return xmo

@app.cell(hide_code=True)
def _(mo):
    mo.md("# List dialect interpreter")
    return


@app.cell(hide_code=True)
def _(mo):
    source = mo.ui.code_editor(
        value="""\
builtin.module {
  func.func @main() {
    %one = arith.constant 1 : i32
    %two = arith.constant 2 : i32
    %three = arith.constant 3 : i32
    %values = list.from_elements %one, %two, %three
        : (i32, i32, i32) -> !list.list<i32>
    %reversed = list.reverse %values : !list.list<i32>
    list.print %reversed : !list.list<i32>
    func.return
  }
}""",
        language="text",
        label="List dialect IR",
        min_height=400,
    )
    return (source,)


@app.cell(hide_code=True)
def _(mo, source, xmo):
    from io import StringIO

    from xdsl.context import Context
    from xdsl.dialects import arith, builtin, func, scf, vector
    from xdsl.frontend.listlang.list_dialect import LIST_DIALECT
    from xdsl.interpreter import Interpreter
    from xdsl.interpreters.arith import ArithFunctions
    from xdsl.interpreters.func import FuncFunctions
    from xdsl.interpreters.list import ListFunctions
    from xdsl.interpreters.scf import ScfFunctions
    from xdsl.interpreters.vector import VectorFunctions
    from xdsl.parser import Parser

    try:
        ctx = Context()
        ctx.load_dialect(builtin.Builtin)
        ctx.load_dialect(arith.Arith)
        ctx.load_dialect(func.Func)
        ctx.load_dialect(scf.Scf)
        ctx.load_dialect(vector.Vector)
        ctx.load_dialect(LIST_DIALECT)

        module = Parser(ctx, source.value).parse_module()
        module.verify()

        output_stream = StringIO()
        interpreter = Interpreter(module, file=output_stream)
        interpreter.register_implementations(ArithFunctions())
        interpreter.register_implementations(FuncFunctions())
        interpreter.register_implementations(ListFunctions())
        interpreter.register_implementations(ScfFunctions())
        interpreter.register_implementations(VectorFunctions())
        interpreter.call_op("main", ())

        output = mo.ui.code_editor(
            value=output_stream.getvalue(),
            language="text",
            disabled=True,
            label="Interpreted result",
            min_height=400,
        )
    except Exception as error:
        notes = getattr(error, "__notes__", ())
        message = "\n".join((*notes, str(error)))
        error_output = mo.ui.code_editor(
            value=message,
            language="text",
            disabled=True,
            label="Error",
            min_height=400,
        )
        output = mo.callout(error_output, kind="danger")

    mo.hstack((source, output), widths="equal", align="start")
    return


if __name__ == "__main__":
    app.run()
