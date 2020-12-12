from django.urls import path
from . import views
from . import botserver

# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('bot',views.index, name='index'),
    path('bot/query/',botserver.botserver, name='query'),
    # path('bot/<str:room_name>/', views.room, name='room'),
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
