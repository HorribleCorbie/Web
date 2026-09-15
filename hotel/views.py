from typing import Any

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


from hotel.models import Room
# Create your views here.

class ShowRoomsView(TemplateView):
    template_name = "rooms/show_rooms.html"

    def get_context_data(self,  **kwargs:Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context
