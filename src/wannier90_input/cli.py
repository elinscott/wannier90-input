"""Command line interface for :mod:`wannier90_input`.

Why does this file exist, and why not put this in ``__main__``?
You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m wannier90_input`` python will
  execute``__main__.py`` as a script. That means there won't be any
  ``wannier90_input.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``wannier90_input.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import click

__all__ = [
    "cli",
]


@click.group()
def main() -> None:
    """CLI for wannier90_input."""
    pass

@main.command()
def update():
    from wannier90_input.fetch import fetch_xml
    from wannier90_input.generate import generate_models
    fetch_xml()
    generate_models()
    
# If you want to have a multi-command CLI, see https://click.palletsprojects.com/en/latest/commands/


if __name__ == "__main__":
    main()
