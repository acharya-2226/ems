import os
from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
from werkzeug.utils import secure_filename
from django.core.exceptions import ValidationError


def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10MB.')

def material_upload_path(instance, filename):
    # Sanitize filename and organize by subject
    filename = secure_filename(filename)
    subject_code = instance.subject.code if instance.subject else 'general'
    return f'materials/{subject_code}/{filename}'

class Material(models.Model):
    title = models.CharField(max_length=200, default='Untitled Material')
    description = models.TextField(blank=True, default='')

    file = models.FileField(
        upload_to=material_upload_path,
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx', 'ppt', 'pptx']),
            validate_file_size
        ],
        default='',
        null=False,
        blank=False,
    )
    
    # ForeignKey to Subject, allow null but default to None explicitly
    subject = models.ForeignKey(
        'core.Subject',
        on_delete=models.CASCADE,
        null=True,
        
        blank=True,
        default=None
    )
    
    # Uploaded by user, cannot be null, but to avoid conflicts, add related_name
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_materials',
        default=None,
        null=False,
        blank=False
    )
    
    is_public = models.BooleanField(default=False)

    # For allowed_roles, keep a default string listing typical roles
    allowed_roles = models.CharField(
        max_length=50,
        default='student,teacher'
    )
    
    # Version string with default '1.0'
    version = models.CharField(
        max_length=10,
        default='1.0'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']
        permissions = [
            ('can_download_material', 'Can download materials'),
        ]

    def __str__(self):
        return f'{self.title} (v{self.version})'
