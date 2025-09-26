FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY jsoncli ./jsoncli
COPY tests ./tests
RUN python -m pip install -U pip && pip install -e ".[query,dev]"
ENTRYPOINT ["python", "-m", "jsoncli.cli"]
