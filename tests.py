from django.test import TestCase

from .models import Donor, BloodRequest


class ModelsImportTest(TestCase):
	def test_models_import_and_basic_fields(self):
		"""Simple test to ensure models import and basic fields work without DB saves."""
		d = Donor(full_name="Test Donor", blood_group="O+", phone="+10000000000", city="TestCity")
		self.assertEqual(d.full_name, "Test Donor")
		self.assertEqual(d.blood_group, "O+")

		br = BloodRequest(requester_name="Requester", phone="+10000000000", blood_group="A+", city="TestCity")
		self.assertEqual(br.requester_name, "Requester")
		self.assertEqual(br.blood_group, "A+")
