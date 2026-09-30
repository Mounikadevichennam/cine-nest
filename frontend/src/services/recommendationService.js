import api from './api';

export const recommendationService = {
  getRecommendedForYou: async () => {
    const res = await api.get('/recommendations/recommended');
    return res.data;
  },

  getBecauseYouWatched: async () => {
    const res = await api.get('/recommendations/because-you-watched');
    return res.data;
  },

  getByGenres: async () => {
    const res = await api.get('/recommendations/by-genres');
    return res.data;
  },

  getByActors: async () => {
    const res = await api.get('/recommendations/by-actors');
    return res.data;
  },

  getTrending: async () => {
    const res = await api.get('/recommendations/trending');
    return res.data;
  },

  getNewReleases: async () => {
    const res = await api.get('/recommendations/new-releases');
    return res.data;
  },

  getContinueWatching: async () => {
    const res = await api.get('/recommendations/continue-watching');
    return res.data;
  },
};
