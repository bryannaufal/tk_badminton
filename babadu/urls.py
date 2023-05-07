from django.urls import path
# from babadu.views import index
from babadu.views import register
from babadu.views import login_user
from babadu.views import logout_user
from babadu.views import show_wishlist

app_name = 'babadu'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout')

]