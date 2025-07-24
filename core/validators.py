from django.core.exceptions import ValidationError
import os

def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB limit
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MB.')

def validate_positive(value):
    if value <= 0:
        raise ValidationError('Value must be positive.')

def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed: {valid_extensions}')
