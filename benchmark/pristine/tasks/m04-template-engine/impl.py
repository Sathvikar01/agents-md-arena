"""Tiny template engine.

render(template, context, escape=False) replaces {{ name }} placeholders:

- names are trimmed of surrounding whitespace inside the braces
- unknown names: placeholder is left completely untouched
- escape=True: substituted values are HTML-escaped (& < >), applied to
  values only, never to surrounding template text
"""
import re


def render(template: str, context: dict, escape: bool = False) -> str:
    def repl(m):
        val = str(context.get(m.group(1), m.group(0)))
        if escape:
            val = (
                val.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
        return val

    return re.sub(r"\{\{(.*)\}\}", repl, template)
