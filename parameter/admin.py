from django.contrib import admin
from parameter.models import Parameter
# Register your models here.

class ParameterAdmin(admin.ModelAdmin):

	list_display = ['id', 'name', 'value', 'createTime']
	search_fields = ['name']
	list_per_page = 20

admin.site.register(Parameter, ParameterAdmin)