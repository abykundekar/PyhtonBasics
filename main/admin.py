# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialSeries
# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
	fieldsets = [
		("Title/date", {"fields" : ["tutorial_title", "tutorial_published"]}),
		("URL", {"fields" : ["tutorial_slug"]}),
		("Series", {"fields" : ["tutorial_series"]}),
		("content", {"fields" : ["tutorial_content"]})
	]

admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)

admin.site.register(Tutorial, TutorialAdmin)