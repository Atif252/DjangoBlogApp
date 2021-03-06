from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from account.api.serializers import RegistrationSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token

from account.models import Account


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0')
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use'
			data['respone'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use'
			data['respone'] = 'Error'
			return Response(data)

		serializers = RegistrationSerializer(data=request.data)

		if serializers.is_valid():
			account = serializers.save()
			data['respone'] = 'Successfully registered new user'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
			return Response(data)
		else:
			data = serializers.errors
		return Response(data)



			# if request.method == 'POST':
	# 	serializers = RegistrationSerializer(data=request.data)
	# 	data = {}
	# 	if serializers.is_valid():
	# 		account = serializers.save()
	# 		data['respone'] = "successfully registered a new user"
	# 		data['email'] = account.email
	# 		data['username'] = account.username
	# 		token = Token.objects.get(user=account).key
	# 		data['token'] = token
	# 	else:
	# 		data = serializers.errors
	# 	return Response(data)





def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email


def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializers = AccountPropertiesSerializer(account)
		return Response(serializers.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "PUT":
		serializers = AccountPropertiesSerializer(account, data=request.data)
		data = {}
		if serializers.is_valid():
			data['respone'] = "Account update success"
			return Response(data=data)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated'
			context['pk'] = account.pk
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)




