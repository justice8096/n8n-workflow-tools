# n8n Workflow Tools
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml ./
COPY src/ ./src/
COPY README.md ./
RUN pip install --no-cache-dir build \
    && python -m build --wheel \
    && pip install --no-cache-dir dist/*.whl

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/n8n-migrate /usr/local/bin/n8n-migrate

WORKDIR /data
ENTRYPOINT ["n8n-migrate"]
CMD ["--help"]
