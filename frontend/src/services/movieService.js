import api from './api';

export const movieService = {
  getMovies: async (params = {}) => {
    const res = await api.get('/movies', { params });
    return res.data;
  },

  getMovieDetails: async (movieId) => {
    const res = await api.get(`/movies/${movieId}`);
    return res.data;
  },

  searchMovies: async (query) => {
    const res = await api.get('/movies/search', { params: { q: query } });
    return res.data;
  },

  recordWatchProgress: async (movieId, progress_seconds, completion_percentage) => {
    const res = await api.post(`/movies/${movieId}/watch`, { movie_id: Number(movieId), progress_seconds, completion_percentage });
    return res.data;
  },

  toggleLike: async (movieId) => {
    const res = await api.post(`/movies/${movieId}/like`);
    return res.data;
  },

  markNotInterested: async (movieId) => {
    const res = await api.post(`/movies/${movieId}/not-interested`);
    return res.data;
  },

  rateMovie: async (movieId, rating) => {
    const res = await api.post(`/movies/${movieId}/rate`, { movie_id: movieId, rating });
    return res.data;
  },
};
