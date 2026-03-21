FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY sawectl/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the CLI script and schema files
COPY sawectl/sawectl.py ./sawectl.py
COPY sawectl/dsl.schema.json ./dsl.schema.json
COPY sawectl/module.schema.json ./module.schema.json

ENTRYPOINT ["python", "sawectl.py"]
