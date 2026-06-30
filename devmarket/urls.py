from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('client/', include('clients.urls')),
    path('developers/', include('clients.developer_urls')),
    path('developers/', include('clients.developer_urls')),
    path('dev/', include('developers.urls')),
    path('projects/', include('projects.urls')),
    path('contracts/', include('contracts.urls')),
    path('store/', include('store.urls')),
    path('payments/', include('payments.urls')),
    path('messages/', include('messaging.urls')),
    path('notifications/', include('notifications.urls')),
    path('reviews/', include('reviews.urls')),
]
