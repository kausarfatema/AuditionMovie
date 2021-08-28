from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')

		else:
			return view_func(request,*args, **kwargs)


	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)

			else:
				return HttpResponse('you are not authorized to view this page')

	return wrapper_func


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None

		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'recruters':
			return redirect('recruter-dash')

		if group == 'talents':
			return redirect('filter-ad')

		if group == 'photographers':
			return redirect('photoappoint')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function


def recruteronly(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None

		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'talents':
			return redirect('filter-ad')

		if group == 'admin':
			return redirect('admin-panel')

		if group == 'photographers':
			return redirect('photoappoint')

		if group == 'recruters':
			return view_func(request, *args, **kwargs)

	return wrapper_function
	

def talentsonly(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None

		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'recruter':
			return redirect('recruter-dash')

		if group == 'admin':
			return redirect('admin-panel')
		
		if group == 'photographers':
			return redirect('photoappoint')

		if group == 'talents':
			return view_func(request, *args, **kwargs)

	return wrapper_function


def photographersonly(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None

		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'recruter':
			return redirect('recruter-dash')

		if group == 'admin':
			return redirect('admin-panel')
		
		if group == 'talents':
			return redirect('filter-ad')

		if group == 'photographers':
			return view_func(request, *args, **kwargs)

	return wrapper_function
	

	
