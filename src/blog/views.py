from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')



	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		context['success_message'] = "Successfully Posted"
		form = CreateBlogPostForm()

	context['form'] = form

	return render(request, 'blog/create_blog.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detail_blog_view(request, slug):

	context = {}

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return redirect('home')
	# blog_post = get_object_or_404(BlogPost, slug=slug)
	# if blog_post.DoesNotExist:
	# 	redirect('home')
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):

	context = {}

	user = request.user

	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
	form = UpdateBlogPostForm(
			initial={
				"title" : blog_post.title,
				"body" : blog_post.body,
				"image" : blog_post.image,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)


def delete_blog_view(request, slug):

	context = {}

	user = request.user

	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return redirect("You don't have permission to delete that")

	context['blog_post'] = blog_post
	operation = blog_post.delete()

	return render(request, 'blog/delete_blog.html', context)



def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))
