import api from "./api";

export const orderService = {
  // Get user's orders
  getAll: async () => {
    const response = await api.get("/orders/");
    return response.data;
  },

  // Get order details
  getById: async (id) => {
    const response = await api.get(`/orders/${id}/`);
    return response.data;
  },

  // Create order
  create: async (orderData) => {
    const response = await api.post("/orders/", orderData);
    return response.data;
  },

  // Cancel order
  cancel: async (id) => {
    const response = await api.post(`/orders/${id}/cancel/`);
    return response.data;
  },
};
