# Task runner.
#
#     just check     # everything that must pass before a commit
#     just fix       # the corrections that can be made automatically
#     just stubs     # create or refresh fa/ from source/
#     just build     # HTML, PDF and EPUB

# Prefer the project venv; fall back to whatever python3 is around.
py := if path_exists(".venv/bin/python") == "true" { ".venv/bin/python" } else { "python3" }

# The checkers are the bargardan-tools package, installed from tools/
# requirements.txt. They are not vendored here and there is no copy to keep in
# sync: three book repositories each carried one and the copies drifted apart,
# which is why the package has a home of its own now.
#
# Nothing in it knows which book it is checking: it reads its config relative
# to the *current directory*, so running it here picks up this project's
# pyproject.toml.
python := py

_default:
    @just --list

# Everything that must pass. check_linebreaks is deliberately absent: it
# enforces one sentence per line, which is right for prose and meaningless for
# verse, and this book is mostly verse. See the note at the foot of pyproject.
check: test
    {{python}} -m bargardan_tools.check_parity --check
    {{python}} -m bargardan_tools.normalize --check
    {{python}} tools/apparatus.py --check

# Only the adapter. The engine has its own suite in the repo it lives in, and
# it must keep passing there without any of this book's config.
test:
    {{python}} -m unittest discover -s tools/tests

# Bidi overrides are reported but never rewritten, so this can still leave
# `just check` failing. That is by design -- a human has to look at those.
fix:
    {{python}} -m bargardan_tools.normalize --fix

# Create or refresh fa/ stubs from source/. Never overwrites existing work.
stubs:
    {{python}} -m bargardan_tools.make_stubs

# Rebuild source/ from the English monolith. Destructive: source/ is generated.
split:
    {{py}} split_book.py

build:
    quarto render

pdf:
    quarto render --to pdf

html:
    quarto render --to html

epub:
    quarto render --to epub

serve:
    quarto preview --port 4200

venv:
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r tools/requirements.txt

clean:
    rm -rf _book .quarto
