import api from './api';

export const adminService = {
  getStats: async () => {
    const res = await api.get('/admin/stats');
    return res.data;
  },

  getAdminMovies: async (skip = 0, limit = 100) => {
    const res = await api.get('/admin/movies', { params: { skip, limit } });
    return res.data;
  },

  createMovie: async (movieData) => {
    const res = await api.post('/admin/movies', movieData);
    return res.data;
  },

  updateMovie: async (movieId, movieData) => {
    const res = await api.put(`/admin/movies/${movieId}`, movieData);
    return res.data;
  },

  deleteMovie: async (movieId) => {
    const res = await api.delete(`/admin/movies/${movieId}`);
    return res.data;
  },
};
