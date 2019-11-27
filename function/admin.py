from django.contrib import admin
from function.models import Function
# Register your models here.
class FuncAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'desc']
	search_fields = ['name']
	list_per_page = 20


admin.site.register(Function)