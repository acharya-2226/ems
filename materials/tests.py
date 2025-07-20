from django.test import TestCase
from .models import Material
from django.core.files.uploadedfile import SimpleUploadedFile


class MaterialModelTest(TestCase):

    def test_material_creation(self):
        material = Material.objects.create(
            title='Sample Material',
            description='Sample description',
            file=SimpleUploadedFile('sample.txt', b'Test content')
        )
        self.assertEqual(str(material), 'Sample Material')
