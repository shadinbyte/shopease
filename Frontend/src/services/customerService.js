import api from "./api";

export const customerService = {
  // Get customer profile
  getProfile: async () => {
    const response = await api.get("/customers/profile/");
    return response.data;
  },

  // Update profile
  updateProfile: async (profileData) => {
    const response = await api.patch("/customers/profile/", profileData);
    return response.data;
  },
};
