import os
import requests

WHATSAPP_API_URL         = os.getenv("WHATSAPP_API_URL", "https://graph.facebook.com")
WHATSAPP_API_VERSION     = os.getenv("WHATSAPP_API_VERSION", "v23.0")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_API_TOKEN       = os.getenv("WHATSAPP_API_TOKEN", "")
WHATSAPP_PUBLIC_BASE_URL = os.getenv("WHATSAPP_PUBLIC_BASE_URL", "http://127.0.0.1:8017")
PDF_OUTPUT_DIR           = os.getenv("PDF_OUTPUT_DIR", "Uploads")


def build_public_pdf_url(filename: str) -> str:
    base = WHATSAPP_PUBLIC_BASE_URL.rstrip("/")
    return f"{base}/Uploads/{filename}"


def _subir_pdf_a_meta(filepath: str, filename: str) -> str | None:
    """Sube el PDF a Meta Media API y retorna el media_id, o None si falla."""
    upload_url = f"{WHATSAPP_API_URL}/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/media"
    headers = {"Authorization": f"Bearer {WHATSAPP_API_TOKEN}"}
    try:
        if not os.path.exists(filepath):
            print(f"[WhatsApp] PDF no encontrado en: {filepath}")
            return None
        with open(filepath, "rb") as f:
            r = requests.post(
                upload_url,
                headers=headers,
                files={"file": (filename, f, "application/pdf")},
                data={"messaging_product": "whatsapp", "type": "application/pdf"},
                timeout=60,
            )
        data = r.json()
        print(f"[WhatsApp] Upload media → Status: {r.status_code} | {data}")
        return data.get("id")
    except Exception as e:
        print(f"[WhatsApp] Error subiendo PDF: {e}")
        return None


def enviar_documento(numero: str, filename: str) -> dict:
    """
    Envía un PDF adjunto a cualquier número de WhatsApp sin necesidad de
    whitelist ni de que el destinatario haya enviado un mensaje previo.

    Estrategia: Document Media Template (un solo request).
    - Se sube el PDF a la Media API de Meta → se obtiene un media_id efímero.
    - Se envía UN template aprobado (tipo UTILITY, header = Documento) con
      el media_id en el componente header.
    - Esto evita el problema del "session window": los templates aprobados
      pueden iniciarse hacia cualquier número en cualquier momento.

    Requisito previo (una sola vez en Meta Business Manager):
      - Crear plantilla llamada 'estado_cartera_doc' (o la que se configure
        en WHATSAPP_TEMPLATE_NAME), categoría UTILITY, idioma es_CO,
        header tipo Documento, body con el texto deseado y esperar aprobación.
    """
    if not WHATSAPP_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        return {
            "ok": False,
            "status": "config_incompleta",
            "message": "Debes configurar WHATSAPP_API_TOKEN y WHATSAPP_PHONE_NUMBER_ID en .env",
        }

    template_name = os.getenv("WHATSAPP_TEMPLATE_NAME", "estado_cartera_doc")
    template_lang = os.getenv("WHATSAPP_TEMPLATE_LANG", "es_CO")

    url = f"{WHATSAPP_API_URL}/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    public_url = build_public_pdf_url(filename)

    try:
        # ── 1. Subir PDF a Meta para obtener media_id ─────────────────────
        pdf_path = os.path.join(os.getcwd(), "Uploads", filename)
        print(f"[WhatsApp] Buscando PDF en: {pdf_path}")
        media_id = _subir_pdf_a_meta(pdf_path, filename)

        if not media_id:
            return {
                "ok": False,
                "status": "error_upload",
                "message": "No se pudo subir el PDF a Meta Media API. Verifica token y permisos.",
                "public_url": public_url,
            }

        # ── 2. Enviar Document Media Template (1 solo request) ────────────
        # El header de tipo 'document' va dentro del template, lo que permite
        # enviar el PDF a cualquier número sin ventana activa de 24 hs.
        payload = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": template_lang},
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "document",
                                "document": {
                                    "id": media_id,
                                    "filename": filename,
                                },
                            }
                        ],
                    }
                ],
            },
        }

        r = requests.post(url, headers=headers, json=payload, timeout=40)
        data = r.json() if r.content else {}
        print(f"[WhatsApp] Document Template → Status: {r.status_code} | Response: {data}")

        return {
            "ok": r.ok,
            "status_code": r.status_code,
            "data": data,
            "public_url": public_url,
        }
    except requests.RequestException as e:
        return {"ok": False, "status": "error_red", "message": str(e)}
