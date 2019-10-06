from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializers = BlogPostSerializer(blog_post)
		return Response(serializers.data)



@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response', "You don't have permission to edit that"})

	if request.method == "PUT":
		serializers = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializers.is_valid():
			serializers.save()
			data["success"] = "update successful"
			return Response(data=data)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response', "You don't have permission to delete that"})

	if request.method == "DELETE":
		operation = blog_post.delete()
		data = {}
		if operation:
			data["success"] = "delete successful"
		else:
			data["failure"] = "delete failed"
		return Response(data=data)



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):

	account = request.user
	
	blog_post = BlogPost(author=account)

	if request.method == "POST":
		serializers = BlogPostSerializer(blog_post, data=request.data)
		if serializers.is_valid():
			serializers.save()
			return Response(serializers.data, status=status.HTTP_201_CREATED)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBlogListView(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter) # Ordering filter for Sorting or Ordering the searched data
	search_fields = ('title', 'body', 'author__username') # Double Underscore is used to specify a particular field within that object of author model