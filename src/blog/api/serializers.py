from rest_framework import serializers

import cv2
import sys
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from blog.models import BlogPost



class BlogPostSerializer(serializers.ModelSerializer):
    
	username = serializers.SerializerMethodField('get_username_from_author')
	# For removing Amazon Web Service Signature from the url
	image = serializers.SerializerMethodField('validate_image_url')

	class Meta:
		model = BlogPost
		fields = ['pk', 'title', 'slug', 'body', 'image', 'date_updated', 'username']

	def get_username_from_author(self, blog_post):
		username = blog_post.author.username
		return username
	# For removing Amazon Web Service Signature from the url
	def validate_image_url(self, blog_post):
		image = blog_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url


class BlogPostUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def validate(self, blog_post):
		try:
			title =blog_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"respone": "Enter a title longer than " + str(MIN_TITLE_LENGTH)})

			body = blog_post['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"respone": "Enter a body longer than " + str(MIN_BODY_LENGTH)})

			image = blog_post['image']
			url = os.path.join(settings.TEMP, str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
				os.remove(url)
				raise serializers.ValidationError({"respone": "That image is too large. Images must be less than 2MB. Try a different image."})

			img = cv2.imread(url)
			dimensions = img.shape # gives: (height, width, ?)

			aspect_ratio = dimensions[1] / dimensions[0]  # divide w/h
			if aspect_ratio < 1:
				os.remove(url)
				raise serializers.ValidationError({"respone": "Image height must not exceed image width. Try a different image."})

			os.remove(url)

		except KeyError:
			pass
		return blog_post



class BlogPostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image', 'date_updated' , 'author']

	def save(self):
		try:
			image = self.validated_data['image']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"respone": "Enter a title longer than " + str(MIN_TITLE_LENGTH)})
			
			body = self.validated_data['body']
			if len(body) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"respone": "Enter a body longer than " + str(MIN_BODY_LENGTH)})

			blog_post = BlogPost(
					author=self.validated_data['author'],
					title=title,
					body=body,
					image=image,
				)

			url = os.path.join(settings.TEMP, str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
				os.remove(url)
				raise serializers.ValidationError({"respone": "That image is too large. Images must be less than 2MB. Try a different image."})

			img = cv2.imread(url)
			dimensions = img.shape # gives: (height, width, ?)

			aspect_ratio = dimensions[1] / dimensions[0]  # divide w/h
			if aspect_ratio < 1:
				os.remove(url)
				raise serializers.ValidationError({"respone": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
			blog_post.save()
			return blog_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title some content and an image"})

		except KeyError:
			pass
		return blog_post



