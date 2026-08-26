import pytest

from semver import parse_version, satisfies, Version


# ---------- parsing ----------

def test_parse_plain():
    v = parse_version("1.22.303")
    assert (v.major, v.minor, v.patch) == (1, 22, 303)
    assert v.prerelease == () and v.build is None


def test_parse_prerelease_and_build():
    v = parse_version("1.2.3-rc.1+exp.sha.5114f85")
    assert (v.major, v.minor, v.patch) == (1, 2, 3)
    assert v.prerelease == ("rc", "1")
    assert v.build == "exp.sha.5114f85"


@pytest.mark.parametrize("bad", [
    "", "1", "1.2", "01.2.3", "1.02.3", "1.2.3-", "1.2.3+",
    "1.2.3-rc..1", "1.2.3-01", "v1.2.3", "1.2.3-rc.01+build",
])
def test_malformed(bad):
    with pytest.raises(ValueError):
        parse_version(bad)


# ---------- ordering ----------

def test_ordering_core():
    assert parse_version("2.0.0") > parse_version("1.9.9")
    assert parse_version("1.10.0") > parse_version("1.9.0")
    assert parse_version("1.0.10") > parse_version("1.0.2")


def test_release_beats_any_prerelease():
    assert parse_version("1.0.0") > parse_version("1.0.0-rc.99")


def test_numeric_lt_alphanumeric():
    assert parse_version("1.0.0-1") < parse_version("1.0.0-alpha")


def test_ascii_compare_and_prefix():
    assert parse_version("1.0.0-alpha.beta") > parse_version("1.0.0-alpha.1")
    assert parse_version("1.0.0-alpha") < parse_version("1.0.0-alpha.1")
    assert parse_version("1.0.0-alpha.beta") < parse_version("1.0.0-beta")


def test_build_ignored_in_equality():
    assert parse_version("1.2.3+b1") == parse_version("1.2.3+b2")


def test_dataclass_shape():
    assert Version(1, 2, 3).prerelease == ()


# ---------- ranges ----------

def test_exact_bare_version():
    assert satisfies("1.2.3", "1.2.3") is True
    assert satisfies("1.2.4", "1.2.3") is False


@pytest.mark.parametrize("spec,v,want", [
    ("^1.2.3", "1.2.3", True),
    ("^1.2.3", "1.9.9", True),
    ("^1.2.3", "2.0.0", False),
    ("^0.2.3", "0.2.9", True),
    ("^0.2.3", "0.3.0", False),
    ("^0.0.3", "0.0.3", True),
    ("^0.0.3", "0.0.4", False),
])
def test_caret(spec, v, want):
    assert satisfies(v, spec) is want


@pytest.mark.parametrize("spec,v,want", [
    ("~1.2.3", "1.2.9", True),
    ("~1.2.3", "1.3.0", False),
    ("~1.2", "1.2.0", True),
    ("~1.2", "1.9.9", False),
])
def test_tilde(spec, v, want):
    assert satisfies(v, spec) is want


@pytest.mark.parametrize("spec,v,want", [
    ("*", "0.0.1", True), ("*", "99.9.9", True),
    ("1.x", "1.9.9", True), ("1.x", "2.0.0", False),
    ("1.2.x", "1.2.7", True), ("1.2.x", "1.3.0", False),
    ("1", "1.5.2", True),
    (">=1.2 <1.6", "1.5.0", True),
    (">=1.2 <1.6", "1.6.0", False),
    ("1.2.x, >=1.2.5", "1.2.7", True),
])
def test_ranges(spec, v, want):
    assert satisfies(v, spec) is want


def test_relational_zero_fill():
    assert satisfies("1.2.9", ">=1.2") is True
    assert satisfies("1.1.9", ">=1.2") is False


# ---------- prerelease gate ----------

def test_prerelease_excluded_from_stable_range():
    assert satisfies("1.3.0-beta", ">=1.2.0") is False
    assert satisfies("2.0.0-rc.1", "*") is False


def test_prerelease_allowed_with_matching_triple():
    assert satisfies("1.3.0-beta", ">=1.3.0-alpha") is True
    assert satisfies("1.3.0-beta", "<=1.3.0-beta") is True


def test_prerelease_wrong_triple_still_excluded():
    assert satisfies("1.4.0-beta", ">=1.3.0-alpha") is False


def test_releases_unaffected_by_gate():
    assert satisfies("1.4.0", ">=1.3.0-alpha") is True
