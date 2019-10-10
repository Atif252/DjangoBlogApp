from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.cache import cache_control
from blog.views import get_blog_queryset
from operator import attrgetter
from blog.models import BlogPost


BLOG_POST_PER_PAGE = 10

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_screen_view(request):

	context = {}

	query = ""

	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("home_screen_view: " + str(query))

	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	

	#Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POST_PER_PAGE)


	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POST_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)


	context['blog_posts'] = blog_posts

	return render(request, 'personal/home.html', context)











	# accounts = Account.objects.all()
	# context['accounts'] = accounts

	# return render(request, 'personal/home.html', context)






	#Example1

	# context['some_string'] = "this is some string that I'm passing to the veiw"
	# context['some_number'] = "141251"

	#Just Another method of passing variables to html file
	# context = {
	# 	'some_string': "this is some string that I'm passing to the veiw",
	# 	'some_number': "141251",
	# }

	#Example 2
	# list_of_values = []
	# list_of_values.append("first entry")
	# list_of_values.append("second entry")
	# list_of_values.append("third entry")
	# list_of_values.append("fourth entry")
	# context["list_of_values"] = list_of_values

	#Example 3
	# questions = Question.objects.all()
	# context['questions'] = questions

	# return render(request, 'personal/home.html', context)