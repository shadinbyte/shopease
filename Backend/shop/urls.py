from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CategoryViewSet,
    CustomerViewSet,
    OrderViewSet,
    ProductViewSet,
    RegisterView,
    analytics_dashboard,
    current_user_view,
    logout_view,
    revenue_by_category,
    top_customers,
    top_selling_products,
)

# Router for ViewSets
router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    # Authentication endpoints
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", logout_view, name="logout"),
    path("auth/user/", current_user_view, name="current_user"),
    # Analytics endpoints
    path("analytics/dashboard/", analytics_dashboard, name="analytics_dashboard"),
    path("analytics/top-products/", top_selling_products, name="top_products"),
    path("analytics/top-customers/", top_customers, name="top_customers"),
    path(
        "analytics/revenue-by-category/",
        revenue_by_category,
        name="revenue_by_category",
    ),
    # Include router URLs
    path("", include(router.urls)),
]
