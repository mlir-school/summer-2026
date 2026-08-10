import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
async def _():
    async def import_xdsl():
        from urllib.parse import urljoin

        import micropip
        from marimo import notebook_location

        location = notebook_location()
        if location is None:
            raise RuntimeError("Could not determine the notebook location")

        # Exported notebooks live at notebooks/html/<name>/ below the site root.
        # Resolve the wheel relative to that root so deployments under a URL prefix
        # (for example, https://host/project/) keep that prefix.
        wheel_url = urljoin(
            f"{str(location).rstrip('/')}/",
            "../../../xdsl-0.0.0-py3-none-any.whl",
        )
        await micropip.install("xdsl @ " + wheel_url)

    await import_xdsl()
    from xdsl.utils import marimo as xmo

    return xmo


@app.cell(hide_code=True)
def _(xmo):
    from xdsl.context import Context
    from xdsl.dialects import builtin, arith, func, scf
    from xdsl.ir import Operation
    from xdsl.printer import Printer
    from typing import Any
    return Any, Context, Operation, Printer, arith, builtin, func, scf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# MLIR IR""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Textual Format""")
    return


@app.cell(hide_code=True)
def _(mo, triangle_text):
    mo.md(
        rf"""
    MLIR uses a textual encoding of the IR for debugging, testing, and storing intermediate representations of programs.
    It can be very useful to take a program at some stage of compilation, and inspect it.
    Let's look at a representation of a function that sums the first `n` integers:

    {mo.ui.code_editor(triangle_text, language="javascript", disabled=True)}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This notebook explains all the components of the above snippet of code. The sections below are structured by _dialect_, which represents a namespace for related abstractions and constructs. More specifically, we look into the
          func, arith and scf dialects """)
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Generic and Custom Format""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    All the snippets that we presented so far are in IRs that follow the _custom format_, a format that allows operations to specify a pretty and concise representation.
    On the other hand, the _generic format_ is a more uniform and verbose representation that unambiguously shows the structure of an operation.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo, triangle_text):
    custom_syntax_editor = mo.ui.code_editor(
        value="""\
    %zero = arith.constant 0 : i32""",
        language="javascript",
        label="**Custom syntax**",
        min_height=10,
    )
    return (custom_syntax_editor,)


@app.cell(hide_code=True)
def _(Parser, ctx, custom_syntax_editor, mo, print_generic):
    try:
        _module = Parser(ctx, custom_syntax_editor.value).parse_module()
        _output = mo.ui.code_editor(
            value=print_generic(_module),
            language="javascript",
            disabled=True,
            label="**Generic syntax**",
            min_height=30,
        )
    except Exception as _error:
        _notes = getattr(_error, "__notes__", ())
        _message = "\n".join((*_notes, str(_error)))
        _error_output = mo.ui.code_editor(
            value=_message,
            language="text",
            disabled=True,
            label="Error",
            min_height=200,
        )
        _output = mo.callout(_error_output, kind="danger")

    mo.vstack(
        (
            mo.md(
                """
                You can edit the custom-syntax MLIR below to see how the generic syntax change.
                """
            ),
            custom_syntax_editor,
            _output,
        )
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Attributes""")
    return


@app.cell(hide_code=True)
def _(builtin, mo):
    mo.md(
        rf"""
    Attributes hold compile-time data, such as constants, types, and other information. Let's look at the attributes in the `arith.constant` operation from earlier:

    {mo.ui.code_editor("%zero = \"arith.constant\"() <{value = 0 : i32}> : () -> i32", language="javascript", disabled=True, min_height=20)}

    The `<{{value = 0 : i32}}>` section represents the static information carried by the operation, which we call **properties**.
    """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## The `builtin` Dialect""")
    return


@app.cell(hide_code=True)
def _(generic_syntax, mo, xmo):
    _empty_module_custom_text = """\
    builtin.module {
    }"""
    _empty_module_generic_text = generic_syntax(
        _empty_module_custom_text, include_module=True
    )
    mo.md(
        rf"""
    The [`builtin` dialect](https://mlir.llvm.org/docs/Dialects/Builtin/) contains the most commonly-used operation in MLIR and xDSL: the `builtin.module` operation.

    A module is a unit of code which holds a single region.
    The smallest possible piece of code in MLIR IR is an empty module:

    **Custom syntax**

    {xmo.module_html(_empty_module_custom_text)}

    **Generic syntax**

    {xmo.module_html(_empty_module_generic_text)}

    When the first operation in a file is not a `builtin.module`, it is implicitly assumed and can be omitted, as is the case for all the snippets below.
    """
    )
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## The `func` Dialect""")
    return


@app.cell(hide_code=True)
def _():
    swap_custom_text = """\
    func.func @swap(%a: i32, %b: i32) -> (i32, i32) {
      func.return %b, %a : i32, i32
    }"""
    return (swap_custom_text,)


@app.cell(hide_code=True)
def _(generic_syntax, mo, swap_custom_text, xmo):
    _swap_generic_text = generic_syntax(swap_custom_text)
    mo.md(
        rf"""
    The [func dialect](https://mlir.llvm.org/docs/Dialects/Func/) contains building blocks to model function definitions and calls.

    **Custom syntax**

    {xmo.module_html(swap_custom_text)}

    **Generic syntax**

    {xmo.module_html(_swap_generic_text)}

    Both snippets represent the same function, which takes two 32-bit integers and returns them in the opposite order.
    There are two operations: `func.func` for the function definition and `func.return` to specify the returned values. All operations in MLIR are prefixed with their dialect name.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Exercise 1: Your First Function

    This function returns its first argument. Can you change it to return the second argument instead?
    """)
    return


@app.cell(hide_code=True)
def _():
    first_text = """\
    func.func @first(%arg0: i32, %arg1: i32) -> i32 {
        func.return %arg0 : i32
    }\
    """
    return (first_text,)


@app.cell(hide_code=True)
def _(first_text, mo):
    first_text_area = mo.ui.code_editor(first_text, language="javascript")
    return (first_text_area,)


@app.cell(hide_code=True)
def _(exercise_text, first_text_area, mo):
    _first_info_text = exercise_text(
        first_text_area.value,
        "first",
        ((1, 2), (3, 4)),
        ("first(1, 2) = ", "first(3, 4) = "),
    )
    mo.vstack((first_text_area, mo.md(_first_info_text)))
    return


@app.cell(hide_code=True)
def _(mo, xmo):
    second_text = """\
    func.func @first(%arg0: i32, %arg1: i32) -> i32 {
        func.return %arg1 : i32
    }\
    """

    mo.accordion({"Solution": xmo.module_html(second_text)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## The `arith` Dialect""")
    return


@app.cell(hide_code=True)
def _():
    add_one_text = """\
    func.func @add_one(%n: i32) -> i32 {
      %one = arith.constant 1 : i32
      %n_plus_one = arith.addi %n, %one : i32
      func.return %n_plus_one : i32
    }"""
    return (add_one_text,)


@app.cell(hide_code=True)
def _(add_one_text, generic_syntax, mo, xmo):
    _add_one_generic_text = generic_syntax(add_one_text)
    mo.md(
        rf"""
    The [arith dialect](https://mlir.llvm.org/docs/Dialects/ArithOps/) contains arithmetic operations on integers, floating-point values, and other numeric constructs. Here is a function that adds one to its only argument:

    **Custom syntax**

    {xmo.module_html(add_one_text)}

    **Generic syntax**

    {xmo.module_html(_add_one_generic_text)}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `i` in `arith.addi` above stands for integer. Some of the operations, like for addition (`addi`/`addf`), subtraction (`subi`/`subf`), multiplication (`muli`/`mulf`), and others have both integer and floating point variants.""")
    return


@app.cell(hide_code=True)
def _():
    less_than_text = """\
    func.func @less_than(%a: i32, %b: i32) -> i1 {
      %slt = arith.cmpi slt, %a, %b : i32
      func.return %slt : i1
    }"""
    return (less_than_text,)


@app.cell(hide_code=True)
def _(generic_syntax, less_than_text, mo, xmo):
    _less_than_generic_text = generic_syntax(less_than_text)
    mo.md(
        rf"""
    The `arith` dialect also contains operations for comparisons. The function below returns the value `true` if a is less than b when the 32-bit values passed in are interpreted as signed integers. Note that the signedness is communicated by the operation itself, not the types of the operands:

    **Custom syntax**

    {xmo.module_html(less_than_text)}

    **Generic syntax**

    {xmo.module_html(_less_than_generic_text)}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""MLIR IR is in [SSA form](https://en.wikipedia.org/wiki/Static_single-assignment_form), meaning that each value can only be assigned to _once_. This property helps reason about the possible runtime data these values can hold, such as whether they are constant, like the SSA value `%one` in the snippet above.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Exercise 2: Multiply and Add""")
    return


@app.cell(hide_code=True)
def _():
    fma_text = """\
    func.func @multiply_and_add(%a: i32, %b: i32, %c: i32) -> (i32) {
      // Change this to return a * b + c instead
      func.return %a : i32
    }"""
    return (fma_text,)


@app.cell(hide_code=True)
def _(fma_text, mo):
    fma_text_area = mo.ui.code_editor(fma_text, language="javascript")
    return (fma_text_area,)


@app.cell(hide_code=True)
def _(exercise_text, fma_text_area, mo):
    _fma_info_text = exercise_text(
        fma_text_area.value,
        "multiply_and_add",
        ((1, 2, 3), (4, 5, 6)),
        ("first(1, 2, 3) = ", "first(4, 5, 6) = "),
    )
    mo.vstack((fma_text_area, mo.md(_fma_info_text)))
    return


@app.cell(hide_code=True)
def _(mo, xmo):
    fma_impl = """\
    func.func @multiply_and_add(%a: i32, %b: i32, %c: i32) -> (i32) {
      %ab = arith.muli %a, %b : i32
      %res = arith.addi %ab, %c : i32
      func.return %res : i32
    }"""

    mo.accordion({"Solution": xmo.module_html(fma_impl)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## The `scf` Dialect""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The [`scf` dialect](https://mlir.llvm.org/docs/Dialects/Scf/) contains operations for structured control flow.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### `scf.if`""")
    return


@app.cell(hide_code=True)
def _():
    select_text = """\
    func.func @select(%cond: i1, %a: i32, %b: i32) -> i32 {
      %res = scf.if %cond -> (i32) {
        scf.yield %a : i32
      } else {
        scf.yield %b : i32
      }
      func.return %res : i32
    }"""
    return (select_text,)


@app.cell(hide_code=True)
def _(generic_syntax, mo, select_text, xmo):
    _select_generic_text = generic_syntax(select_text)
    mo.md(
        rf"""
    Here is a function that returns the second argument if the first argument is `true`, and the third argument otherwise:

    **Custom syntax**

    {xmo.module_html(select_text)}

    **Generic syntax**

    {xmo.module_html(_select_generic_text)}

    Note that we did not put early returns in the branches of the `scf.if` operation.
    This is due to MLIR's SSA blocks adhering to a specific contract: operations within a block are executed sequentially from top to bottom, and each operation is guaranteed to complete and yield control back to the outer block.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Exercise 3: Abs Function""")
    return


@app.cell(hide_code=True)
def _(abs_function_text, mo):
    abs_input_text = mo.ui.text("-5")
    abs_text_area = mo.ui.code_editor(abs_function_text, language="javascript")
    return abs_input_text, abs_text_area


@app.cell(hide_code=True)
def _():
    abs_function_text = """\
    func.func @abs(%a: i32) -> i32 {
        %false = arith.constant 0 : i1
        %res = scf.if %false -> (i32) {
            scf.yield %a : i32
        } else {
            scf.yield %a : i32
        }
        func.return %res : i32
    }"""
    return (abs_function_text,)


@app.cell(hide_code=True)
def _(Parser, abs_input_text, abs_text_area, ctx, run_func):
    abs_error_text = ""
    abs_results_text = ""
    try:
        abs_input = int(abs_input_text.value)
        abs_inputs = (abs_input,)
        abs_module = Parser(ctx, abs_text_area.value).parse_module()
        abs_results = run_func(abs_module, "abs", abs_inputs)
        abs_results_text = f"abs({abs_input}) = {abs_results}"
    except Exception as e:
        abs_error_text = str(e)

    if abs_error_text:
        abs_info_text = f"""
        Error:

        ```
        {abs_error_text}
        ```
        """
    else:
        abs_info_text = f"""\
        Change the definition of `abs` to compute the absolute value of the input.

        ```
        {abs_results_text}
        ```
        """
    return (abs_info_text,)


@app.cell
def _(abs_info_text, abs_input_text, abs_text_area, mo):
    mo.vstack(
        (
            mo.md(f"""Input: {abs_input_text} {mo.ui.button(label="run")}"""),
            abs_text_area,
            mo.md(abs_info_text),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo, xmo):
    abs_impl = """\
    func.func @abs(%a: i32) -> i32 {
        %zero = arith.constant 0 : i32
        %slt = arith.cmpi slt, %a, %zero : i32
        %res = scf.if %slt -> (i32) {
            %r = arith.subi %zero, %a : i32
            scf.yield %r : i32
        } else {
            scf.yield %a : i32
        }
        func.return %res : i32
    }"""

    mo.accordion({"Solution": xmo.module_html(abs_impl)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### `scf.for`""")
    return


@app.cell(hide_code=True)
def _(generic_syntax, mo, triangle_text, xmo):
    _triangle_generic_text = generic_syntax(triangle_text)
    mo.md(
        rf"""
    The `scf` dialect also contains abstractions to represent for loops. For example,
    to caclulate the [triangular number](https://en.wikipedia.org/wiki/Triangular_number) 1 + 2 + 3 + ... + n:

    **Custom syntax**

    {xmo.module_html(triangle_text)}

    **Generic syntax**

    {xmo.module_html(_triangle_generic_text)}

    Due to the SSA contract, we cannot accumulate by updating a value.
    Instead, the loop body takes some number of immutable values and yields the same number of values to use for the next loop.
    When all iterations are complete, these values are returned by the operation.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Exercise 4: Factorial Function""")
    return


@app.cell(hide_code=True)
def _(mo, triangle_text):
    second_input_text = mo.ui.text("5")
    second_text_area = mo.ui.code_editor(
        triangle_text.replace("triangle", "factorial"), language="javascript"
    )
    return second_input_text, second_text_area


@app.cell(hide_code=True)
def _(Parser, ctx, run_func, second_input_text, second_text_area):
    second_error_text = ""
    second_results_text = ""
    try:
        second_input = int(second_input_text.value)
        second_inputs = (second_input,)
        second_module = Parser(ctx, second_text_area.value).parse_module()
        second_results = run_func(second_module, "factorial", second_inputs)
        second_results_text = f"factorial({second_input}) = {second_results}"
    except Exception as e:
        second_error_text = str(e)

    if second_error_text:
        second_info_text = f"""
        Error:

        ```
        {second_error_text}
        ```
        """
    else:
        second_info_text = f"""\
        Change the definition of `factorial` to compute the factorial of the input, instead of the triangle.
        Assume that the input is non-negative.

        ```
        {second_results_text}
        ```
        """
    return (second_info_text,)


@app.cell(hide_code=True)
def _(mo, second_info_text, second_input_text, second_text_area):
    mo.vstack(
        (
            mo.md(f"""Input: {second_input_text} {mo.ui.button(label="run")}"""),
            second_text_area,
            mo.md(second_info_text),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo, xmo):
    fact_impl = """\
    func.func @factorial(%n: i32) -> i32 {
      %zero = arith.constant 0 : i32
      %one = arith.constant 1 : i32
      %n_plus_one = arith.addi %n, %one : i32
      %res = scf.for %i = %one to %n_plus_one step %one iter_args(%acc_in = %one) -> (i32) : i32 {
        %acc_out = arith.muli %acc_in, %i : i32
        scf.yield %acc_out : i32
      }
      func.return %res : i32
    }"""

    mo.accordion({"Solution": xmo.module_html(fact_impl)})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Generic/Custom syntax playground""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Here is another playground to experiment with the custom and generic syntax.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo, triangle_text):
    custom_syntax_editor2 = mo.ui.code_editor(
        value=triangle_text,
        language="javascript",
        label="**Custom syntax**",
    )
    return (custom_syntax_editor2,)


@app.cell(hide_code=True)
def _(Parser, ctx, custom_syntax_editor, mo, print_generic):
    try:
        _module = Parser(ctx, custom_syntax_editor.value).parse_module()
        _output = mo.ui.code_editor(
            value=print_generic(_module),
            language="javascript",
            disabled=True,
            label="**Generic syntax**",
        )
    except Exception as _error:
        _notes = getattr(_error, "__notes__", ())
        _message = "\n".join((*_notes, str(_error)))
        _error_output = mo.ui.code_editor(
            value=_message,
            language="text",
            disabled=True,
            label="Error",
        )
        _output = mo.callout(_error_output, kind="danger")

    mo.vstack(
        (
            mo.md(
                """
                Edit the custom-syntax MLIR below to see its generic syntax.
                """
            ),
            custom_syntax_editor,
            _output,
        )
    )
    return


@app.cell(hide_code=True)
def _(Operation, Printer, StringIO):
    def print_generic(op: Operation) -> str:
        io = StringIO()
        Printer(io, print_generic_format=True).print_op(op)
        return io.getvalue()
    return


@app.cell(hide_code=True)
def _(Context, arith, builtin, func, scf):
    ctx = Context()
    ctx.load_dialect(builtin.Builtin)
    ctx.load_dialect(func.Func)
    ctx.load_dialect(scf.Scf)
    ctx.load_dialect(arith.Arith)
    return (ctx,)


@app.cell(hide_code=True)
def _():
    triangle_text = """\
    func.func @triangle(%n: i32) -> i32 {
      %zero = arith.constant 0 : i32
      %one = arith.constant 1 : i32
      %n_plus_one = arith.addi %n, %one : i32
      %res = scf.for %i = %one to %n_plus_one step %one iter_args(%acc_in = %zero) -> (i32) : i32 {
        %acc_out = arith.addi %acc_in, %i : i32
        scf.yield %acc_out : i32
      }
      func.return %res : i32
    }\
    """
    return (triangle_text,)


@app.cell(hide_code=True)
def _(ctx, triangle_text):
    # parse triangle module to make sure it's valid IR

    from io import StringIO

    from xdsl.parser import Parser, Input

    triangle_module = Parser(ctx, triangle_text, "").parse_module()
    # triangle_module
    return Parser, StringIO


@app.cell(hide_code=True)
def _(Parser, ctx, print_generic):
    def generic_syntax(source: str, *, include_module: bool = False) -> str:
        module = Parser(ctx, source).parse_module()
        module.verify()
        op = module if include_module else module.body.ops.first
        return print_generic(op)

    return (generic_syntax,)


@app.cell(hide_code=True)
def _(Any, builtin):
    def run_func(module: builtin.ModuleOp, name: str, args: tuple[Any, ...]):
        from xdsl.interpreter import Interpreter
        from xdsl.interpreters import scf, arith, func

        interpreter = Interpreter(module)
        interpreter.register_implementations(scf.ScfFunctions)
        interpreter.register_implementations(arith.ArithFunctions)
        interpreter.register_implementations(func.FuncFunctions)

        res = interpreter.call_op(name, args)

        if len(res) == 1:
            res = res[0]

        return res
    return (run_func,)


@app.cell(hide_code=True)
def _(Any, Parser, ctx, run_func):
    def exercise_text(
        module_text: str,
        function_name: str,
        inputs: tuple[Any, ...],
        formats: tuple[str, ...],
    ) -> str:
        error_text = ""
        results_text = ""
        try:
            module = Parser(ctx, module_text).parse_module()
            results_text = "\n".join(
                format + str(run_func(module, function_name, input))
                for format, input in zip(formats, inputs, strict=True)
            )
        except Exception as e:
            error_text = str(e)
        if error_text:
            info_text = f"""
    Error:

    ```
    {error_text}
    ```
    """
        else:
            info_text = f"""
    Here are the outputs when running the function:

    ```
    {results_text}
    ```
    """
        return info_text
    return (exercise_text,)



if __name__ == "__main__":
    app.run()
