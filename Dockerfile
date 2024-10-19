FROM python:3.12.7-slim-bookworm
ARG now
ENV now=$now
WORKDIR /app/src/term_assist/test
COPY . /app/
RUN python3 -m pip install /app[develop]
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN python3 -m pipx completions
RUN python3 -m pytest test.py --junit-xml=output/${now}_output.xml | tee output/${now}_output.log
