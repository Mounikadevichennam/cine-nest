import api from './api';

export const authService = {
  signup: async (name, email, password, preferred_language = "Telugu") => {
    const res = await api.post('/auth/signup', { name, email, password, preferred_language });
    if (res.data.access_token) {
      localStorage.setItem('cinenest_token', res.data.access_token);
    }
    return res.data;
  },

  login: async (email, password) => {
    const res = await api.post('/auth/login', { email, password });
    if (res.data.access_token) {
      localStorage.setItem('cinenest_token', res.data.access_token);
    }
    return res.data;
  },

  getCurrentUser: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  },

  logout: () => {
    localStorage.removeItem('cinenest_token');
    localStorage.removeItem('cinenest_profile');
  },
};
