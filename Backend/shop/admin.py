from django.contrib import admin

from .models import Category, Customer, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "is_active", "created_at"]
    list_filter = ["category", "is_active", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["price", "stock", "is_active"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "city", "created_at"]
    search_fields = ["user__username", "user__email", "phone"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ["subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "status", "total_amount", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["customer__user__username", "customer__user__email"]
    inlines = [OrderItemInline]
    readonly_fields = ["total_amount", "created_at", "updated_at"]
