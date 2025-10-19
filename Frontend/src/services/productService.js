import api from "./api";

export const productService = {
  // Get all products
  getAll: async (params = {}) => {
    const response = await api.get("/products/", { params });
    return response.data;
  },

  // Get single product
  getById: async (id) => {
    const response = await api.get(`/products/${id}/`);
    return response.data;
  },

  // Search products
  search: async (query) => {
    const response = await api.get("/products/", {
      params: { search: query },
    });
    return response.data;
  },

  // Filter by category
  getByCategory: async (categoryId) => {
    const response = await api.get("/products/", {
      params: { category: categoryId },
    });
    return response.data;
  },
};
