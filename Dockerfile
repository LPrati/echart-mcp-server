FROM python:3.12-slim

WORKDIR /app

# Install uv using the official installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set environment to use system Python
ENV UV_SYSTEM_PYTHON=1

COPY pyproject.toml ./

RUN uv pip install --system --no-cache .

COPY formatters.py ./
COPY echart_server.py ./

CMD ["python", "echart_server.py", "--host", "0.0.0.0", "--port", "8000"]