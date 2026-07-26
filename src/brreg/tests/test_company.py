from django.test import TestCase

from brreg.models import Company


class CompanyTestCase(TestCase):
    def setUp(self) -> None:
        Company.objects.create(navn="Strong company", organisasjonsnummer="123456789")
        Company.objects.create(navn="Weak company", organisasjonsnummer="444456749")

    def test_companies_are_correctly_identified(self) -> None:
        """Companies are correctly identified by their organization numbers"""
        strong = Company.objects.get(organisasjonsnummer="123456789")
        weak = Company.objects.get(organisasjonsnummer="444456749")
        self.assertEqual(strong.navn, "Strong company")
        self.assertEqual(weak.navn, "Weak company")
