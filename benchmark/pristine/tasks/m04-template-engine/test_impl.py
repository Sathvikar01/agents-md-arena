from impl import render


def test_simple_substitution():
    assert render("Hello {{name}}!", {"name": "Ada"}) == "Hello Ada!"


def test_multiple_placeholders_same_line():
    assert render("{{a}}+{{b}}={{c}}", {"a": 1, "b": 2, "c": 3}) == "1+2=3"


def test_names_trimmed():
    assert render("Hi {{  name  }}", {"name": "Bo"}) == "Hi Bo"


def test_missing_key_left_untouched():
    assert render("[{{nope}}]", {}) == "[{{nope}}]"
    assert render("{{a}} {{missing}}", {"a": "x"}) == "x {{missing}}"


def test_escape_applies_to_values_only():
    out = render("{{v}} <br>", {"v": "<b>&"}, escape=True)
    assert out == "&lt;b&gt;&amp; <br>"


def test_no_escape_by_default():
    assert render("{{v}}", {"v": "<i>"}) == "<i>"


def test_non_string_values_coerced():
    assert render("n={{n}}", {"n": 42}) == "n=42"


def test_empty_template_and_context():
    assert render("", {}) == ""
