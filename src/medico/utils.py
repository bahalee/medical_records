import os
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

def save_uploaded_file(uploaded_file):
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    return fs.url(filename)

def format_datetime(dt):
    return dt.strftime("%d %B %Y, %H:%M")

def get_current_year():
    return timezone.now().year

def is_valid_image(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1].lower()
    return ext in valid_extensions

def generate_unique_filename(instance, filename):
    base, ext = os.path.splitext(filename)
    unique_filename = f"{base}_{timezone.now().strftime('%Y%m%d_%H%M%S')}{ext}"
    return unique_filename