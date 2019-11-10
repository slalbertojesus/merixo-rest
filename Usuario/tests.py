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
        accountOne = Account.objects.get(name='Paola Marai')
        accountTwo = Account.objects.get(name='Fernando Mikhail')
        self.assertEqual(accountOne.name, "Paola Marai")
        self.assertEqual(accountTwo.name, "Fernando Mikhail")
        