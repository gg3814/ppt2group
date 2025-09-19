from werkzeug.utils import secure_filename
from pathlib import Path
import logging

log = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(file) -> str:
    filename = secure_filename(file.filename) or "upload.pptx"
    filepath = UPLOAD_DIR / filename;
    try:
        file.save(filepath)
    except Exception:
        raise RuntimeError("파일 저장 중 예외 발생") 

    file.close()
    log.info("File save: path=%s", filepath);
    return str(filepath);