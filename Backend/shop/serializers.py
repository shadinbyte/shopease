from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Customer, Order, OrderItem, Product


# User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        # Automatically create customer profile
        Customer.objects.create(user=user)
        return user


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_product_count(self, obj):
        return obj.products.count()


# Product Serializers
class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "category",
            "category_name",
            "image",
            "is_active",
            "is_in_stock",
        ]
        read_only_fields = ["id", "is_in_stock"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "category_name",
            "image",
            "is_active",
            "is_in_stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_in_stock", "created_at", "updated_at"]


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "user",
            "username",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "full_name",
            "created_at",
        ]
        read_only_fields = ["id", "user", "full_name", "created_at"]


# Order Item Serializers
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_image",
            "quantity",
            "price",
            "subtotal",
        ]
        read_only_fields = ["id", "price", "subtotal"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]

        if not product.is_active:
            raise serializers.ValidationError(
                {"product": "This product is not available."}
            )

        if quantity > product.stock:
            raise serializers.ValidationError(
                {"quantity": f"Only {product.stock} items available in stock."}
            )

        return attrs


# Order Serializers
class OrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "status",
            "total_amount",
            "items_count",
            "created_at",
        ]
        read_only_fields = ["id", "total_amount", "created_at"]

    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "total_amount",
            "shipping_address",
            "order_notes",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "total_amount", "created_at", "updated_at"]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["shipping_address", "order_notes", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        # Get customer from authenticated user
        customer = self.context["request"].user.customer_profile

        # Create order
        order = Order.objects.create(customer=customer, **validated_data)

        # Create order items and update stock
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            # Create order item
            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=product.price
            )

            # Update product stock
            product.stock -= quantity
            product.save()

        # Calculate and save total
        order.calculate_total()

        return order
