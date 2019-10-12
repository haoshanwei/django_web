from django.contrib import admin
from items.models import Items, ItemsApplication
# Register your models here.

class ItemsAdmin(admin.ModelAdmin):
	list_per_page = 20
	list_display = ['id', 'name', 'desc', 'member', 'startTime', 'endTime']
	search_fields = ['name']
	actions_on_top = True
	actions_on_bottom = False


class ItemsApplicationAdmin(admin.ModelAdmin):
	list_per_page = 20
	list_display = ['id', 'name', 'desc', 'member', 'createTime']
	search_fields = ['name']
	actions_on_top = True
	actions_on_bottom = False

admin.site.register(Items, ItemsAdmin)

admin.site.register(ItemsApplication, ItemsApplicationAdmin)



