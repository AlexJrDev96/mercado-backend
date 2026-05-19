import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_folder():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads")


def save_product_image(file):
    if not file or not file.filename:
        return None, "Nenhum arquivo enviado"

    if not allowed_file(file.filename):
        return None, "Formato não permitido. Use PNG, JPG, JPEG, GIF ou WEBP."

    upload_folder = get_upload_folder()
    os.makedirs(upload_folder, exist_ok=True)

    extension = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{extension}"
    safe_name = secure_filename(filename)
    file.save(os.path.join(upload_folder, safe_name))

    return f"/uploads/{safe_name}", None
