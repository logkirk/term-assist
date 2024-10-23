FROM python:3.12.7-slim-bookworm
WORKDIR /app/src/term_assist/test
COPY . /app/
RUN python3 -m pip install /app[develop]
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN python3 -m pipx completions
