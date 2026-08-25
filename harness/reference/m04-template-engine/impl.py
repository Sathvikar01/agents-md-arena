import re


def render(template: str, context: dict, escape: bool = False) -> str:
    def repl(m):
        key = m.group(1).strip()
        if key not in context:
            return m.group(0)
        val = str(context[key])
        if escape:
            val = (
                val.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
        return val

    return re.sub(r"\{\{\s*([^{}]+?)\s*\}\}", repl, template)
