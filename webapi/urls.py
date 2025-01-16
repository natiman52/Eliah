from django.urls import path
from . import views
from user import views as user_views


urlpatterns = [
    path('',views.home),
    path('women',views.female),
    path('men',views.male),
    path('kids',views.kids),
    path("detail/<int:id>",views.get_detail),
    path('create-subscribers',views.create_subscriber),
    path('get-token',user_views.GetToken.as_view())


]