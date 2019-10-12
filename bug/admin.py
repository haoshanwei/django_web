from django.contrib import admin
from bug.models import Bug
# Register your models here.

class BugAdmin(admin.ModelAdmin):
	list_display = ['id', 'bugname', 'bugdesc', 'bugimgFile', 'bugstatus', 'buglevel',
					'bugcreater', 'bugrepair', 'createtime', 'closetime']
	search_fields = ['bugname']
	list_per_page = 20


admin.site.register(Bug)