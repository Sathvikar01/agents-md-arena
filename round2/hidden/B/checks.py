"""Structural refactor checks for round-2 track B.

score2.py imports this module and calls:
    count_for(app_name) -> int
    run_checks(app_dir: Path, app_name) -> dict[check_name -> bool]
"""

import ast
from pathlib import Path


def _src(adir: Path, name: str) -> str:
    p = adir / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _tree(src: str):
    try:
        return ast.parse(src)
    except SyntaxError:
        return None


def _funcs(tree):
    return {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)} \
        if tree else {}


def _classes(tree):
    return {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)} \
        if tree else {}


def _fully_hinted(fn: ast.FunctionDef) -> bool:
    args = [a for a in fn.args.args if a.arg != "self"]
    annotated_args = all(a.annotation is not None for a in args)
    return annotated_args and fn.returns is not None


# ----------------------------- orders_app ---------------------------------

def check_taxes_module(adir: Path) -> bool:
    src = _src(adir, "taxes.py")
    if "TAX_RATE" not in src or "def tax(" not in src:
        return False
    for py in adir.glob("*.py"):
        if py.name == "taxes.py" or py.name.startswith("test_"):
            continue
        if "0.08" in py.read_text(encoding="utf-8"):
            return False
    # main and pricing must actually use it
    return "import taxes" in _src(adir, "main.py") and \
        "import taxes" in _src(adir, "pricing.py")


def check_no_orders_global(adir: Path) -> bool:
    src = _src(adir, "store.py")
    return "ORDERS" not in src


def check_order_store_class(adir: Path) -> bool:
    t = _tree(_src(adir, "store.py"))
    cls = _classes(t).get("OrderStore")
    if not cls:
        return False
    methods = {n.name for n in cls.body if isinstance(n, ast.FunctionDef)}
    return {"save_order", "get_order", "clear"} <= methods


def check_wrappers_kept(adir: Path) -> bool:
    fns = _funcs(_tree(_src(adir, "store.py")))
    return {"save_order", "get_order", "clear"} <= set(fns)


def check_split_functions(adir: Path) -> bool:
    fns = _funcs(_tree(_src(adir, "main.py")))
    return {"validate_order", "price_order", "process_order"} <= set(fns)


def check_legacy_utils_gone(adir: Path) -> bool:
    return not (adir / "legacy_utils.py").exists()


def check_discount_rate(adir: Path) -> bool:
    src = _src(adir, "pricing.py")
    fns = _funcs(_tree(src))
    if "discount_rate" not in fns:
        return False
    apply_src = ast.get_source_segment(src, fns["apply_discounts"]) or ""
    return "discount_rate(" in apply_src


def check_type_hints(adir: Path) -> bool:
    for mod in ("main.py", "pricing.py", "store.py"):
        fns = _funcs(_tree(_src(adir, mod)))
        public = [f for n, f in fns.items() if not n.startswith("_")]
        if not public or not all(_fully_hinted(f) for f in public):
            return False
    tsrc = _src(adir, "taxes.py")
    tfns = _funcs(_tree(tsrc))
    return "tax" in tfns and _fully_hinted(tfns["tax"])


# ----------------------------- logalyzer_app ------------------------------

def check_report_uses_parser(adir: Path) -> bool:
    src = _src(adir, "report.py")
    return 'split("|"' not in src and "parse_line" in src and \
        "parser" in _src(adir, "report.py")


def check_consts_module(adir: Path) -> bool:
    src = _src(adir, "consts.py")
    return "MINUTE_SECONDS" in src and "60" in src


def check_no_bare_60_in_stats(adir: Path) -> bool:
    import re as _re
    return not _re.search(r"\b60\b", _src(adir, "stats.py"))


def check_logstats_class(adir: Path) -> bool:
    t = _tree(_src(adir, "stats.py"))
    cls = _classes(t).get("LogStats")
    if not cls:
        return False
    methods = {n.name for n in cls.body if isinstance(n, ast.FunctionDef)}
    return {"levels", "minutes"} <= methods


def check_delegation_kept(adir: Path) -> bool:
    fns = _funcs(_tree(_src(adir, "stats.py")))
    return {"level_counts", "minute_counts"} <= set(fns)


def check_analyze_v2_deleted(adir: Path) -> bool:
    return "analyze_v2" not in _src(adir, "stats.py")


def check_summarize_renamed(adir: Path) -> bool:
    src = _src(adir, "stats.py")
    return "def summarize" in src and "def f(" not in src


def check_maxsplit_used(adir: Path) -> bool:
    return "maxsplit=2" in _src(adir, "parser.py")


CHECKS = {
    "orders_app": {
        "taxes_module": check_taxes_module,
        "no_orders_global": check_no_orders_global,
        "order_store_class": check_order_store_class,
        "wrappers_kept": check_wrappers_kept,
        "split_functions": check_split_functions,
        "legacy_utils_gone": check_legacy_utils_gone,
        "discount_rate": check_discount_rate,
        "type_hints": check_type_hints,
    },
    "logalyzer_app": {
        "report_uses_parser": check_report_uses_parser,
        "consts_module": check_consts_module,
        "no_bare_60_in_stats": check_no_bare_60_in_stats,
        "logstats_class": check_logstats_class,
        "delegation_kept": check_delegation_kept,
        "analyze_v2_deleted": check_analyze_v2_deleted,
        "summarize_renamed": check_summarize_renamed,
        "maxsplit_used": check_maxsplit_used,
    },
}


def run_checks(adir: Path, app: str) -> dict:
    return {name: fn(adir) for name, fn in CHECKS[app].items()}


def count_for(app: str) -> int:
    return len(CHECKS[app])
