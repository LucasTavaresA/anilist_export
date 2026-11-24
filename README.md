# anilist export

Export your anilist to a excel spreadsheet.

## Usage

```sh
al_export
```

## Just run it (requires uv)

```sh
uvx --from git+https://github.com/lucastavaresa/anilist_export al_export
```

Or run after cloning the repo:

```sh
git clone https://github.com/lucastavaresa/anilist_export.git
cd anilist_export
uv run al_export
```

## Install

- uv:

```sh
git clone https://github.com/lucastavaresa/anilist_export.git
cd anilist_export
uv tool install .
al_export
```

- pipx:

```sh
git clone https://github.com/lucastavaresa/anilist_export.git
cd anilist_export
pipx install .
al_export
```

- Without pipx:

```sh
git clone https://github.com/lucastavaresa/anilist_export.git
cd anilist_export
python -m venv .venv
source .venv/bin/activate # check: https://docs.python.org/3.13/library/venv.html#how-venvs-work
pip install -r requirements.txt
python main.py
```
