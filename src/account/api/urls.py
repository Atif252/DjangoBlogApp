from django.urls import path
from account.api.views import(
 	registration_view,
 	update_account_view,
 	account_properties_view,
 	ObtainAuthTokenView,
 )

app_name = "account"

urlpatterns = [
	path('register', registration_view, name="register"),
	path('login', ObtainAuthTokenView.as_view(), name="login"),
	path('properties', account_properties_view, name="properties"),
	path('properties/update', update_account_view, name="update"),
	
]