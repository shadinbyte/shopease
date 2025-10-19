import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { ShoppingBag, CreditCard } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { orderService } from '../services/orderService';
import { formatCurrency } from '../utils/helpers';
import { toast } from 'sonner';

export default function Checkout() {
  const { cart, getCartTotal, clearCart } = useCart();
  const { profile } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      shipping_address: profile?.address
        ? `${profile.address}, ${profile.city} ${profile.postal_code}`
        : '',
    },
  });

  const onSubmit = async (data) => {
    if (cart.length === 0) {
      toast.error('Your cart is empty');
      return;
    }

    setLoading(true);
    try {
      const orderData = {
        shipping_address: data.shipping_address,
        order_notes: data.order_notes || '',
        items: cart.map((item) => ({
          product: item.id,
          quantity: item.quantity,
        })),
      };

      const order = await orderService.create(orderData);
      clearCart();
      toast.success('Order placed successfully!');
      navigate(`/orders/${order.id}`);
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to place order';
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <ShoppingBag className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-2">Your cart is empty</h2>
        <p className="text-gray-600 mb-6">Add some products to checkout</p>
        <Button onClick={() => navigate('/products')}>
          Browse Products
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Checkout</h1>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Checkout Form */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Shipping Address</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="shipping_address">Full Address *</Label>
                  <Input
                    id="shipping_address"
                    type="text"
                    placeholder="123 Main St, New York, NY 10001"
                    {...register('shipping_address', {
                      required: 'Shipping address is required',
                    })}
                  />
                  {errors.shipping_address && (
                    <p className="text-sm text-red-500">
                      {errors.shipping_address.message}
                    </p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="order_notes">Order Notes (Optional)</Label>
                  <textarea
                    id="order_notes"
                    rows="3"
                    placeholder="Any special instructions for your order"
                    className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    {...register('order_notes')}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <CreditCard className="h-5 w-5" />
                  <span>Payment Method</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-800">
                    💳 Cash on Delivery (COD) is currently the only payment method available.
                    You'll pay when your order arrives.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Order Summary */}
          <div>
            <Card className="sticky top-24">
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {cart.map((item) => (
                    <div key={item.id} className="flex justify-between text-sm">
                      <div className="flex-1">
                        <p className="font-medium truncate">{item.name}</p>
                        <p className="text-gray-600">
                          {item.quantity} × {formatCurrency(item.price)}
                        </p>
                      </div>
                      <p className="font-medium">
                        {formatCurrency(item.price * item.quantity)}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="border-t pt-4 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal</span>
                    <span className="font-medium">
                      {formatCurrency(getCartTotal())}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Shipping</span>
                    <span className="font-medium text-green-600">Free</span>
                  </div>
                  <div className="flex justify-between text-lg font-bold border-t pt-2">
                    <span>Total</span>
                    <span className="text-primary">
                      {formatCurrency(getCartTotal())}
                    </span>
                  </div>
                </div>

                <Button type="submit" className="w-full" size="lg" disabled={loading}>
                  {loading ? 'Placing Order...' : 'Place Order'}
                </Button>

                <p className="text-xs text-center text-gray-600">
                  By placing your order, you agree to our terms and conditions
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </form>
    </div>
  );
}
