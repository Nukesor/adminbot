default: run

run:
    poetry run python main.py run

setup:
    poetry install

lint:
    poetry run black --check adminbot
    poetry run isort \
        --skip __init__.py \
        --check-only adminbot
    poetry run flake8 adminbot

format:
    # remove unused imports
    poetry run autoflake \
        --remove-all-unused-imports \
        --recursive \
        --exclude=__init__.py,.venv \
        --in-place adminbot
    poetry run black adminbot
    poetry run isort adminbot \
        --skip __init__.py


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
