FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --uid 10001 --create-home agent
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir pydantic fastapi uvicorn httpx pytest
COPY app ./app
COPY evals ./evals
USER 10001
CMD ["uvicorn","app.api:app","--host","0.0.0.0","--port","8000"]
