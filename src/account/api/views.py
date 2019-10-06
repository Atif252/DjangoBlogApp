from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import RegistrationSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST', ])
def registration_view(request):

	if request.method == 'POST':
		serializers = RegistrationSerializer(data=request.data)
		data = {}
		if serializers.is_valid():
			account = serializers.save()
			data['respone'] = "successfully registered a new user"
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializers.errors
		return Response(data)


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













