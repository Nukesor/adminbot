default: run

run:
    poetry run python main.py run

setup:
    poetry install

lint:
    poetry run ruff check ./adminbot --output-format=full
    poetry run ruff format ./adminbot --diff

format:
    poetry run ruff check --fix ./adminbot
    poetry run ruff format ./adminbot


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
