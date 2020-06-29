# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
# Create your views here.

def single_slug(request, single_slug):
	categories = [c.category_slug for c in TutorialCategory.objects.all()]
	if single_slug in categories:
		matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
		
		series_urls = {}
		for m in matching_series:
			part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
			series_urls[m] = part_one.tutorial_slug
		return render(request,
					  "main/category.html",
					  {"part_ones": series_urls})

	tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
	if single_slug in tutorials:
		this_tutorial = Tutorial.objects.get(tutorial_slug = single_slug)
		tutSeries = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")

		this_tutorial_index = list(tutSeries).index(this_tutorial)

		return render(request,
					  "main/tutorial.html",
					  {"tutorial": this_tutorial,
					   "sidebar" : tutSeries,
					   "this_tutorial_index" : this_tutorial_index})

	return HttpResponse("%s does not corresond to anything!!" %single_slug)

def homepage(request):
	return render(request = request, 
		template_name = "main/categories.html",
		context = {"categories" : TutorialCategory.objects.all})

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.get_username()
			messages.success(request, 'New Account Created : %s'%username)
			auth_login(request, user)
			messages.info(request, "you are now logged in as %s" %username)
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, "%s : %s" %{msg} %{form.error_messages[msg]})
 
	form = NewUserForm
	return render(request, 
		"main/register.html",
		{"form" : form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			user = form.get_user()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				auth_login(request, user)
				messages.info(request, "you are logged in as %s" %username)
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid UserName or Password")
		else:
			messages.error(request, "Invalid data!")


	form = AuthenticationForm()
	return render(request = request, 
		template_name = "main/login.html",
		context = {"form" : form})

def logout_request(request):
	logout(request)
	messages.info(request, "You logged out Successfully!")
	return redirect("main:homepage")