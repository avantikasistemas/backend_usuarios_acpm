import os
from datetime import time
from dotenv import load_dotenv

load_dotenv() # Carga las variables desde el archivo .env

# Accesos
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
MICROSOFT_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID")
MICROSOFT_API_SCOPE = ['https://graph.microsoft.com/.default']

# URLs
MICROSOFT_URL = os.getenv("MICROSOFT_URL")
MICROSOFT_URL_GRAPH = os.getenv("MICROSOFT_URL_GRAPH")

# Datos correo
PARENT_FOLDER=os.getenv("PARENT_FOLDER")
TARGET_FOLDER=os.getenv("TARGET_FOLDER")
EMAIL_USER=os.getenv("EMAIL_USER")

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "cambia-este-secreto")

# Horario laboral
START_WORK_HOUR = time(7, 30)
END_WORK_HOUR = time(17, 30)