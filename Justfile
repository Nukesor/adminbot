default: run

run:
    poetry run python main.py run

setup:
    poetry install

lint:
    poetry run black --check adminbot
    poetry run isort --check-only adminbot
    poetry run flake8 adminbot

format:
    # remove unused imports
    poetry run autoflake \
        --remove-all-unused-imports \
        --recursive \
        --in-place adminbot
    poetry run black adminbot
    poetry run isort adminbot


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
