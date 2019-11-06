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

@api_view(['POST',])
@permission_classes([AllowAny,])
def api_create_usuario_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save() 
			data['response'] = "se registró de forma exitosa"
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user = account).key
			data['token'] = token
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

