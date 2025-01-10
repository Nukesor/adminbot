default: run

run:
    uv run ./main.py run

setup:
    uv sync

lint:
    uv run ruff check ./adminbot --output-format=full
    uv run ruff format ./adminbot --diff

format:
    uv run ruff check --fix ./adminbot
    uv run ruff format ./adminbot


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
