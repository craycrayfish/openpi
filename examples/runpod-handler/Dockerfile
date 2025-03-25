FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /
COPY . /
RUN uv sync

# Start the container
CMD ["uv", "run", "python", "runpod_handler/rp_handler.py"]