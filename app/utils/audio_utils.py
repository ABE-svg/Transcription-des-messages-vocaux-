
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):

    allowed_extensions = {"wav", "mp3", "m4a", "flac"}    

    if "." not in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1].lower()
    
    return ext in allowed_extensions


def save_temp_file(file):
    filename = secure_filename(file.filename)
    temp_path = f"/tmp/{filename}"
    file.save(temp_path)
    return temp_path