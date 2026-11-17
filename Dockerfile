FROM python:3.11-slim

WORKDIR /app

# Evita que Python escriba archivos .pyc y fuerza salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements_bot.txt .
RUN pip install --no-cache-dir -r requirements_bot.txt

COPY . .

# Puerto por defecto para la nube
EXPOSE 8080

CMD ["python", "-m", "src.telegram_bot.bot_cloud"]
