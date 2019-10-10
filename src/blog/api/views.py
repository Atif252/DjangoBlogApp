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
from blog.api.serializers import BlogPostSerializer, BlogPostUpdateSerializer, BlogPostCreateSerializer


SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'



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
		serializers = BlogPostUpdateSerializer(blog_post, data=request.data, partial=True)
		data = {}
		if serializers.is_valid():
			serializers.save()
			data["respone"] = UPDATE_SUCCESS
			data["pk"] = blog_post.pk
			data["title"] = blog_post.title
			data["body"] = blog_post.body
			data["slug"] = blog_post.slug
			data["date_updated"] = blog_post.date_updated
			image_url = str(request.build_absolute_uri(blog_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_urlf.rfind("?")]
			data['image'] = image_url
			data['username'] = blog_post.author.username
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
			data["success"] = DELETE_SUCCESS
		else:
			data["failure"] = "delete failed"
		return Response(data=data)



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):

	if request.method == 'POST':

		data = request.data
		data['author'] = request.user.pk
		serializers = BlogPostCreateSerializer(data=data)

		data = {}
		if serializers.is_valid():
			blog_post = serializers.save()
			data["respone"] = CREATE_SUCCESS
			data["pk"] = blog_post.pk
			data["title"] = blog_post.title
			data["body"] = blog_post.body
			data["slug"] = blog_post.slug
			data["date_updated"] = blog_post.date_updated
			image_url = str(request.build_absolute_uri(blog_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_urlf.rfind("?")]
			data['image'] = image_url
			data['username'] = blog_post.author.username
			return Response(data=data)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiBlogListView(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter) # Ordering filter for Sorting or Ordering the searched data
	search_fields = ('title', 'body', 'author__username') # Double Underscore is used to specify a particular field within that object of author model