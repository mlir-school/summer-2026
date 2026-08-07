import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full")


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
def _(mo):
    mo.md("# ListLang frontend compiler")
    return


@app.cell(hide_code=True)
def _(mo):
    source = mo.ui.code_editor(
        value="""\
let values = [1, 2, 3];
values.push_front(0).reverse()""",
        language="rs",
        label="ListLang",
        min_height=400,
    )
    return (source,)


@app.cell(hide_code=True)
def _(mo, source, xmo):
    from xdsl.context import Context as _Context
    from xdsl.frontend.listlang.lowerings import WrapModuleInFunc
    from xdsl.frontend.listlang.main import program_to_mlir_module
    from xdsl.frontend.listlang.source import ParseError

    compiled_module = None
    try:
        compiled_module = program_to_mlir_module(source.value)
        WrapModuleInFunc().apply(_Context(), compiled_module)
        compiled_module.verify()
        output = mo.ui.code_editor(
            value=str(compiled_module),
            language="javascript",
            disabled=True,
            label="Generated IR",
            min_height=400,
        )
    except ParseError as error:
        line, column = error.line_column(source.value)
        lines = source.value.split("\n")
        first_line = max(1, line - 1)
        last_line = min(len(lines), line + 1)
        gutter_width = len(str(last_line))
        excerpt_lines: list[str] = []

        for line_number in range(first_line, last_line + 1):
            marker = ">" if line_number == line else " "
            source_line = lines[line_number - 1].rstrip("\r").expandtabs()
            excerpt_lines.append(
                f"{marker} {line_number:>{gutter_width}} | {source_line}"
            )
            if line_number == line:
                raw_prefix = lines[line_number - 1][: column - 1]
                display_column = len(raw_prefix.expandtabs())
                excerpt_lines.append(
                    f"  {' ' * gutter_width} | {' ' * display_column}^"
                )

        error_location = mo.md(
            f"""\
**Parse error:** {error.msg}<br>
Line {line}, column {column}"""
        )
        error_excerpt = mo.ui.code_editor(
            value="\n".join(excerpt_lines),
            language="text",
            disabled=True,
            label="Source location",
            min_height=80,
        )
        output = mo.callout(
            mo.vstack((error_location, error_excerpt), gap=0),
            kind="danger",
        )

    mo.hstack((source, output), widths="equal", align="start")
    return (compiled_module,)


@app.cell(hide_code=True)
def _(compiled_module, mo, xmo):
    from xdsl.frontend.listlang import marimo as listlang_marimo

    result = None
    if compiled_module is not None:
        try:
            result = mo.ui.code_editor(
                value=listlang_marimo.interp_main(compiled_module),
                language="text",
                disabled=True,
                label="Interpreted result",
                min_height=100,
            )
        except Exception as _error:
            _notes = getattr(_error, "__notes__", ())
            _message = "\n".join((*_notes, str(_error)))
            _error_output = mo.ui.code_editor(
                value=_message,
                language="text",
                disabled=True,
                label="Interpretation error",
                min_height=100,
            )
            result = mo.callout(_error_output, kind="danger")

    result
    return


if __name__ == "__main__":
    app.run()
