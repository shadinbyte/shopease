import api from "./api";

export const categoryService = {
  // Get all categories
  getAll: async () => {
    const response = await api.get("/categories/");
    return response.data;
  },

  // Get products in category
  getProducts: async (categoryId) => {
    const response = await api.get(`/categories/${categoryId}/products/`);
    return response.data;
  },
};
