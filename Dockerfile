# ===== Base Image =====
FROM python:3.13-slim

# ===== Working directory inside the container =====
WORKDIR /app

# ===== Copy project files =====
COPY . .

# ===== Install dependencies =====
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ===== Create data folders if they don't exist =====
RUN mkdir -p data/raw data/processed

# ===== Default command: run only the analysis =====
CMD ["python", "scripts/text_analysis.py"]
# To run other scripts, override the command when running the container, e.g.:
