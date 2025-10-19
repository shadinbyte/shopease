from django.contrib.auth.models import User
from django.db.models import Count, F, Sum
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Customer, Order, OrderItem, Product
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


# Authentication Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"])
    def products(self, request, pk=None):
        """Get all products in this category"""
        category = self.get_object()
        products = category.products.filter(is_active=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        # Filter by category
        category = self.request.query_params.get("category", None)
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by stock availability
        in_stock = self.request.query_params.get("in_stock", None)
        if in_stock == "true":
            queryset = queryset.filter(stock__gt=0)

        # Search by name
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.select_related("category")

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """Get products with low stock (less than 10)"""
        products = Product.objects.filter(stock__lt=10, stock__gt=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get", "put", "patch"])
    def profile(self, request):
        """Get or update current user's profile"""
        try:
            customer = request.user.customer_profile
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method in ["PUT", "PATCH"]:
            partial = request.method == "PATCH"
            serializer = CustomerSerializer(
                customer, data=request.data, partial=partial
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        return OrderListSerializer

    def get_queryset(self):
        user = self.request.user

        # Admin can see all orders, regular users only their own
        if user.is_staff:
            return Order.objects.all().select_related("customer__user")

        return Order.objects.filter(customer__user=user).select_related(
            "customer__user"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Return detailed order information
        detail_serializer = OrderDetailSerializer(order)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()

        if order.status in ["shipped", "delivered"]:
            return Response(
                {"error": "Cannot cancel shipped or delivered orders"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Restore product stock
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()

        order.status = "cancelled"
        order.save()

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


# Analytics Views
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analytics_dashboard(request):
    """Get overall analytics dashboard data"""

    data = {
        "total_products": Product.objects.filter(is_active=True).count(),
        "total_categories": Category.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "total_revenue": Order.objects.filter(
            status__in=["delivered", "shipped"]
        ).aggregate(Sum("total_amount"))["total_amount__sum"]
        or 0,
    }

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def top_selling_products(request):
    """Get top 10 best-selling products"""

    products = Product.objects.annotate(
        total_sold=Sum("order_items__quantity")
    ).order_by("-total_sold")[:10]

    data = []
    for product in products:
        data.append(
            {
                "id": product.id,
                "name": product.name,
                "total_sold": product.total_sold or 0,
                "price": product.price,
                "stock": product.stock,
            }
        )

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def top_customers(request):
    """Get top 10 customers by total spending"""

    customers = Customer.objects.annotate(
        total_spent=Sum("orders__total_amount"), order_count=Count("orders")
    ).order_by("-total_spent")[:10]

    data = []
    for customer in customers:
        data.append(
            {
                "id": customer.id,
                "name": customer.full_name,
                "email": customer.user.email,
                "total_spent": customer.total_spent or 0,
                "order_count": customer.order_count,
            }
        )

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def revenue_by_category(request):
    """Get revenue breakdown by category"""

    categories = Category.objects.annotate(
        total_revenue=Sum("products__order_items__subtotal")
    ).order_by("-total_revenue")

    data = []
    for category in categories:
        data.append(
            {
                "id": category.id,
                "name": category.name,
                "total_revenue": float(category.total_revenue or 0),
            }
        )

    return Response(data)
