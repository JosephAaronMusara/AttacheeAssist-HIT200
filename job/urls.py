from django.contrib import admin
from django.urls import path , include
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobapp.urls')),
    path('', include('account.urls')),
   # path('__debug__/', include('debug_toolbar.urls')),

]
