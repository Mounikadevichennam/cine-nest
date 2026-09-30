import React, { useState, useEffect } from 'react';
import { Save, AlertCircle } from 'lucide-react';

export default function MovieForm({ initialData = null, onSubmit, loading = false }) {
  const [formData, setFormData] = useState({
    title: '',
    language: 'Telugu',
    release_year: 2024,
    imdb_rating: 8.0,
    imdb_votes: 1000,
    poster_url: '',
    trailer_url: '',
    storyline: '',
    imdb_id: '',
    genre_names: 'Action, Drama',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || '',
        language: initialData.language || 'Telugu',
        release_year: initialData.release_year || 2024,
        imdb_rating: initialData.imdb_rating || 0.0,
        imdb_votes: initialData.imdb_vote_count || 0,
        poster_url: initialData.poster_url || '',
        trailer_url: initialData.trailer_url || '',
        storyline: initialData.storyline || initialData.description || '',
        imdb_id: initialData.imdb_id || '',
        genre_names: initialData.genres ? initialData.genres.map(g => g.name).join(', ') : 'Action, Drama',
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!formData.poster_url.trim()) {
      setError('Poster URL is required for catalog insertion.');
      return;
    }

    const payload = {
      ...formData,
      release_year: parseInt(formData.release_year),
      imdb_rating: parseFloat(formData.imdb_rating),
      imdb_votes: parseInt(formData.imdb_votes),
      genre_names: formData.genre_names.split(',').map(g => g.trim()).filter(Boolean),
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-[#141824] p-8 rounded-2xl border border-gray-800 space-y-6 shadow-xl max-w-3xl">
      {error && (
        <div className="p-3 bg-red-950/60 border border-red-800 text-red-300 text-xs rounded-lg flex items-center space-x-2">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <label className="block text-xs font-semibold text-gray-300 mb-1">Movie Title *</label>
          <input 
            type="text" 
            name="title"
            required
            value={formData.title}
            onChange={handleChange}
            placeholder="e.g. Pushpa 2: The Rule"
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-300 mb-1">Language *</label>
          <select 
            name="language"
            value={formData.language}
            onChange={handleChange}
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          >
            <option value="Telugu">Telugu</option>
            <option value="Hindi">Hindi</option>
            <option value="Tamil">Tamil</option>
            <option value="Malayalam">Malayalam</option>
            <option value="Kannada">Kannada</option>
            <option value="English">English</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-300 mb-1">Release Year (2016-2026) *</label>
          <input 
            type="number" 
            name="release_year"
            min={2016}
            max={2026}
            required
            value={formData.release_year}
            onChange={handleChange}
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-300 mb-1">IMDb / TMDB Rating (0.0 to 10.0)</label>
          <input 
            type="number" 
            name="imdb_rating"
            step="0.1"
            min={0}
            max={10}
            value={formData.imdb_rating}
            onChange={handleChange}
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="sm:col-span-2">
          <label className="block text-xs font-semibold text-gray-300 mb-1">Poster Image URL (Required) *</label>
          <input 
            type="url" 
            name="poster_url"
            required
            value={formData.poster_url}
            onChange={handleChange}
            placeholder="https://image.tmdb.org/t/p/w500/..."
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="sm:col-span-2">
          <label className="block text-xs font-semibold text-gray-300 mb-1">Trailer Embed URL (Optional)</label>
          <input 
            type="url" 
            name="trailer_url"
            value={formData.trailer_url}
            onChange={handleChange}
            placeholder="https://www.youtube.com/embed/..."
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="sm:col-span-2">
          <label className="block text-xs font-semibold text-gray-300 mb-1">Genres (Comma-separated)</label>
          <input 
            type="text" 
            name="genre_names"
            value={formData.genre_names}
            onChange={handleChange}
            placeholder="Action, Crime, Drama"
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="sm:col-span-2">
          <label className="block text-xs font-semibold text-gray-300 mb-1">Storyline / Description</label>
          <textarea 
            name="storyline"
            rows={4}
            value={formData.storyline}
            onChange={handleChange}
            placeholder="Synopsis of the movie..."
            className="w-full px-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-xs text-white focus:outline-none focus:border-red-500"
          />
        </div>
      </div>

      <div className="flex items-center justify-end pt-4 border-t border-gray-800">
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-lg flex items-center space-x-2 shadow-lg shadow-red-950/50 transition"
        >
          <Save className="w-4 h-4" />
          <span>{loading ? 'Saving Movie...' : 'Save Movie Record'}</span>
        </button>
      </div>
    </form>
  );
}
