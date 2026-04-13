import base64
import logging
import os
import re

import requests
from flask import Flask, make_response, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("ecg_receiver")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

ORTHANC_URL = os.environ.get("ORTHANC_URL", "http://orthanc:8042")

_SUCCESS_XML = (
    '<?xml version="1.0" encoding="UTF-16"?>'
    '<dicomresponse xmlns="http://philips.com">'
    "<status>SUCCESS</status>"
    "</dicomresponse>"
).encode("utf-16")


@app.route("/", defaults={"path": ""}, methods=["POST"])
@app.route("/<path:path>", methods=["POST"])
def philips_handler(path):
    raw = request.get_data()
    try:
        text = raw.decode("utf-16")
    except Exception:
        text = raw.decode("utf-8", errors="ignore")

    match = re.search(r"<dicomdata>(.*?)</dicomdata>", text, re.DOTALL)
    if not match:
        log.warning("Requisicao sem <dicomdata> de %s", request.remote_addr)
        return "Aguardando", 400

    try:
        dicom_bytes = base64.b64decode(match.group(1).strip())
    except Exception as exc:
        log.error("Falha ao decodificar base64: %s", exc)
        return "Bad Request", 400

    try:
        resp = requests.post(
            f"{ORTHANC_URL}/instances",
            data=dicom_bytes,
            headers={"Content-Type": "application/dicom"},
            timeout=30,
        )
        resp.raise_for_status()
        instance_id = resp.json().get("ID", "?")
        log.info("DICOM enviado ao Orthanc: instance=%s de %s", instance_id, request.remote_addr)
    except Exception as exc:
        log.error("Falha ao enviar pro Orthanc: %s", exc)
        return "Internal Server Error", 500

    res = make_response(_SUCCESS_XML)
    res.headers["Content-Type"] = "text/xml; charset=utf-16"
    return res, 200


if __name__ == "__main__":
    from waitress import serve
    log.info("ECG Receiver iniciando na porta 8080")
    serve(app, host="0.0.0.0", port=8080)
