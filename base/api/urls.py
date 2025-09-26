from django.urls import path
from .import views

#Tip learned here: Anytime you create a file for your urls,
# you need to configure it in django urls main so that it can recognize the url
#After you create your urls path over here for the first time, go to urls.py in your main project not app
# Then import include then use it like this, ('folder_name/', include('app.api.urls'))

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>', views.getRoom)
]