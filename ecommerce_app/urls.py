from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from ecommerce import views as e_views
from accounts import urls as a_urls
from payments.views import CreateCheckoutSessionView, ProductLandingPageView, SuccessView, CancelView



router = SimpleRouter()

router.register(r'products', e_views.ProductViewSet, basename='products')
router.register(r'categories', e_views.CategoryViewSet, basename='categories')
router.register(r'cart_items', e_views.CartItemViewSet, basename='cartitem')



urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='checkout'),
    path('landing/', ProductLandingPageView.as_view(), name='landing'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls + a_urls.urlpatterns
