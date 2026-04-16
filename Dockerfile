# Dockerfile para Backend FastAPI con SQL Server
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias básicas
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Agregar repositorio de Microsoft
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg

# Configurar repositorio para Debian 11
RUN echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list

# Instalar ODBC Driver 17
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear carpeta Uploads si no existe
RUN mkdir -p /app/Uploads

# Exponer puerto
EXPOSE 8017

# Comando de inicio
CMD ["python3", "main.py"]
