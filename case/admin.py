from django.contrib import admin
from items.models import ItemsApplication, Items
from django.db import models
from case.models import Apitest, Apistep, SingeApi


# Register your models here.
class ApistepAdmin(admin.TabularInline):
	list_display =['id', 'apiname', 'apiurl', 'apiheaders', 'apiparamvalue', 'apimethod', 'apistatuscode',
				   'apiresult', 'apistatus', 'create_time', 'apitest']
	model = Apistep
	extra = 1



class ApitestAdmin(admin.ModelAdmin):
	list_display = ['id', 'apitestname', 'apitester', 'apitestresult', 'create_time']
	inlines = [ApistepAdmin]
	search_fields = ['apitestname']
	list_per_page = 20


class SingeApiAdmin(admin.ModelAdmin):
	list_display = ['id', 'apiname', 'apidesc', 'apiurl', 'apiparamvalue', 'apimethod', 'apistatuscode',
					'apiresult', 'create_time', 'update_time']
	search_fields = ['apitestname']
	list_per_page = 20


admin.site.register(Apitest, ApitestAdmin)
admin.site.register(SingeApi, SingeApiAdmin)
