import api from "./api";

export const authService = {
  // Register new user
  register: async (userData) => {
    const response = await api.post("/auth/register/", userData);
    if (response.data.access) {
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
    }
    return response.data;
  },

  // Login
  login: async (credentials) => {
    const response = await api.post("/auth/login/", credentials);
    if (response.data.access) {
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
    }
    return response.data;
  },

  // Logout
  logout: async () => {
    const refreshToken = localStorage.getItem("refresh_token");
    try {
      await api.post("/auth/logout/", { refresh_token: refreshToken });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get("/auth/user/");
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem("access_token");
  },
};
