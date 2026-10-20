from typing import Any

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json
 
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from hotel.models import Room
# Create your views here.
 
class ShowRoomsView(TemplateView):
    template_name = "rooms/show_rooms.html"

    def get_context_data(self,  **kwargs:Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context
