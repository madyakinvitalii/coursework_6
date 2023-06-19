from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from skymarket import settings
from users.views import CustomUserViewSet

# ----------------------------------------------------------------
# router for users based on Djoser
router = SimpleRouter()


# ----------------------------------------------------------------
# register route
router.register('users', CustomUserViewSet, basename='users')


# ----------------------------------------------------------------
# urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/redoc-tasks/', SpectacularRedocView.as_view(url_name='schema')),
    path('api/ads/', include('ads.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
]


# ----------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
