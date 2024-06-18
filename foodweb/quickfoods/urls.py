from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index.html'),
    path('signup', views.signup, name ='signup.html'),
    path('signin', views.signin, name= 'signin.html'),
    path('logout',views.logout, name='logout.html'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart.html'),
    path('create_food_item', views.create_food_item, name='create_food_item'),
   # Add more paths as needed
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)