from django.test import TestCase
from .models import Account

#Test module for Account model
class AccountModelTest(TestCase):
    def setUp(self):
        Account.objects.create(
            name='Paola Marai', email='maraibenitez@hotmail.com', password='Cesar6969', username='paola257')
        Account.objects.create(
            name='Fernando Mikhail', email='fernix@gmail.com', password='coolguy827', username='fernix')

    def test_account_model(self):
        puppy_casper = Account.objects.get(name='Casoer')
        puppy_muffin = Account.objects.get(name='Muffin')
        self.assertEqual(
            puppy_casper.get_breed(), "Casper belongs to Bull Dog breed.")
        self.assertEqual(
            puppy_muffin.get_breed(), "Muffin belongs to Gradane breed.")


