FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /opt/todolist

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHON_PATH=/opt/todolist

RUN groupadd --system service && useradd --system -g service api

RUN pip install "poetry==1.2.0"

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi --no-root

COPY src/ ./
# COPY docker-entrypoint.sh ./entrypoint.sh

USER api

ENTRYPOINT ["bash", "docker-entrypoint.sh"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

# --platform=linux/amd64