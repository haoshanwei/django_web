from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from items.models import Items, ItemsApplication
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def item(request):
	username = request.session.get('user', '')
	if username is None:
		return HttpResponseRedirect("/login/")
	else:
		item_list = Items.objects.all()
		item_app_list = ItemsApplication.objects.all()
		return render(request, 'item.html', {"user": username, "items": item_list, 'apps': item_app_list})


