from django.test import TestCase
from .models import Account

#Test module for Account model
class AccountModelTest(TestCase):
    def setUp(self):
        Account.objects.create(
            name='Casper', email='', password='Bull Dog', username='Black')
        Account.objects.create(
            name='Casper', email='', password='Bull Dog', username='Black')

    def test_account_model(self):
        puppy_casper = Account.objects.get(name='Casper')
        puppy_muffin = Account.objects.get(name='Muffin')
        self.assertEqual(
            puppy_casper.get_breed(), "Casper belongs to Bull Dog breed.")
        self.assertEqual(
            puppy_muffin.get_breed(), "Muffin belongs to Gradane breed.")


