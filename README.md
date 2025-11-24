# anilist export

Export your anilist to a excel spreadsheet.

## Usage

```sh
al_export
```

## Install

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
