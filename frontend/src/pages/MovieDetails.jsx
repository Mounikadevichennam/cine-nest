import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { movieService } from '../services/movieService';
import { Play, Film, ThumbsUp, EyeOff, Star, Calendar, Globe, ArrowLeft, VideoOff, Award } from 'lucide-react';

export default function MovieDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [liked, setLiked] = useState(false);
  const [notInterested, setNotInterested] = useState(false);
  const [userRating, setUserRating] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const data = await movieService.getMovieDetails(id);
        setMovie(data);
      } catch (err) {
        console.error("Failed to load movie details:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDetails();
  }, [id]);

  const handleLike = async () => {
    try {
      const res = await movieService.toggleLike(id);
      setLiked(res.liked);
    } catch (err) {
      console.error(err);
    }
  };

  const handleNotInterested = async () => {
    try {
      await movieService.markNotInterested(id);
      setNotInterested(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleRate = async (stars) => {
    try {
      await movieService.rateMovie(id, stars);
      setUserRating(stars);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B0D12] flex items-center justify-center text-white font-mono text-xs">
        Loading Movie Details...
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="min-h-screen bg-[#0B0D12] text-white pt-24 px-6 text-center">
        <Navbar />
        <h2 className="text-2xl font-bold">Movie Not Found</h2>
        <Link to="/home" className="text-red-500 hover:underline text-xs mt-4 inline-block">Return to Home</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white pt-20 pb-20">
      <Navbar />

      <div className="max-w-6xl mx-auto px-6 space-y-8">
        {/* Back Link */}
        <Link to="/home" className="inline-flex items-center space-x-1.5 text-xs text-gray-400 hover:text-white transition pt-4">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Feed</span>
        </Link>

        {/* Hero Banner Backdrop container if available */}
        {movie.backdrop_url && (
          <div className="relative h-64 sm:h-80 rounded-2xl overflow-hidden border border-gray-800 shadow-2xl">
            <img src={movie.backdrop_url} alt={movie.title} className="w-full h-full object-cover filter brightness-50" />
            <div className="absolute inset-0 bg-gradient-to-t from-[#0B0D12] via-black/40 to-transparent" />
          </div>
        )}

        {/* Details Card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 bg-[#141824] p-6 sm:p-8 rounded-2xl border border-gray-800 shadow-2xl">
          {/* Poster */}
          <div className="aspect-[2/3] w-full max-w-xs mx-auto md:max-w-none rounded-xl overflow-hidden shadow-2xl border border-gray-700">
            <img src={movie.poster_url} alt={movie.title} className="w-full h-full object-cover" />
          </div>

          {/* Details Column */}
          <div className="md:col-span-2 space-y-5">
            <div>
              <div className="flex items-center space-x-2 text-xs font-semibold text-red-500 uppercase tracking-wider mb-2">
                <span>{movie.language}</span>
                <span>•</span>
                <span>{movie.country || 'India'}</span>
                {movie.original_title && movie.original_title !== movie.title && (
                  <>
                    <span>•</span>
                    <span className="text-gray-400 normal-case">Orig: {movie.original_title}</span>
                  </>
                )}
              </div>
              <h1 className="text-3xl sm:text-5xl font-black tracking-tight">{movie.title}</h1>
              {movie.director && (
                <p className="text-xs text-gray-400 mt-1">Directed by <span className="text-gray-200 font-semibold">{movie.director}</span></p>
              )}
            </div>

            {/* Metadata Pills */}
            <div className="flex flex-wrap items-center gap-3 text-xs text-gray-300">
              <div className="flex items-center space-x-1 bg-amber-500/10 border border-amber-500/30 px-3 py-1 rounded-full text-amber-400 font-bold">
                <Star className="w-3.5 h-3.5 fill-current" />
                <span>{movie.imdb_rating ? `${movie.imdb_rating.toFixed(1)} / 10` : 'N/A'}</span>
                {movie.imdb_vote_count > 0 && <span className="text-gray-400 font-normal">({movie.imdb_vote_count.toLocaleString()} votes)</span>}
              </div>

              <div className="flex items-center space-x-1 bg-gray-800 px-3 py-1 rounded-full text-gray-300">
                <Calendar className="w-3.5 h-3.5" />
                <span>{movie.release_year}</span>
              </div>
            </div>

            {/* Genres */}
            <div className="flex flex-wrap gap-2">
              {movie.genres?.map((g) => (
                <span key={g.id} className="px-3 py-1 bg-gray-800/80 text-gray-300 rounded-md text-xs font-medium border border-gray-700">
                  {g.name}
                </span>
              ))}
            </div>

            {/* Storyline */}
            <div>
              <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Storyline</h3>
              <p className="text-sm text-gray-300 leading-relaxed">{movie.storyline || movie.description || "No overview available for this film."}</p>
            </div>

            {/* Action Bar */}
            <div className="pt-4 border-t border-gray-800 space-y-4">
              <div className="flex flex-wrap items-center gap-3">
                {/* Watch Feature Film Button */}
                <button 
                  onClick={() => navigate(`/watch/${movie.id}?mode=movie`)}
                  className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold text-sm rounded-lg flex items-center space-x-2 shadow-lg shadow-red-950/50 transition transform hover:scale-105"
                >
                  <Play className="w-4 h-4 fill-current" />
                  <span>Play Movie</span>
                </button>

                {/* Watch Official Trailer Button */}
                {movie.trailer_url ? (
                  <button 
                    onClick={() => navigate(`/watch/${movie.id}?mode=trailer`)}
                    className="px-5 py-3 bg-gray-800 hover:bg-gray-700 text-gray-200 font-semibold text-sm rounded-lg flex items-center space-x-2 border border-gray-700 transition"
                  >
                    <Film className="w-4 h-4 text-red-500" />
                    <span>Watch Trailer</span>
                  </button>
                ) : (
                  <span className="px-4 py-2.5 bg-gray-900 text-gray-500 text-xs font-medium rounded-lg flex items-center space-x-1.5 border border-gray-800">
                    <VideoOff className="w-4 h-4" />
                    <span>Trailer Unavailable</span>
                  </span>
                )}

                {/* Like Button */}
                <button 
                  onClick={handleLike}
                  className={`px-4 py-2.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition border ${
                    liked 
                      ? 'bg-red-950/60 border-red-600 text-red-400' 
                      : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  <ThumbsUp className="w-4 h-4" />
                  <span>{liked ? 'Liked' : 'Like'}</span>
                </button>

                {/* Not Interested Button */}
                <button 
                  onClick={handleNotInterested}
                  disabled={notInterested}
                  className={`px-4 py-2.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition border ${
                    notInterested 
                      ? 'bg-gray-900 border-gray-800 text-gray-500 cursor-not-allowed' 
                      : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  <EyeOff className="w-4 h-4" />
                  <span>{notInterested ? 'Hidden' : 'Not Interested'}</span>
                </button>
              </div>

              {/* Star Rating Widget */}
              <div className="flex items-center space-x-2 pt-2">
                <span className="text-xs font-medium text-gray-400">Your Rating:</span>
                <div className="flex items-center space-x-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button 
                      key={star}
                      onClick={() => handleRate(star)}
                      className="p-1 focus:outline-none hover:scale-125 transition"
                    >
                      <Star className={`w-4 h-4 ${star <= userRating ? 'text-amber-400 fill-current' : 'text-gray-600'}`} />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Trailer Embed Section */}
        {movie.trailer_url ? (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                <Film className="w-5 h-5 text-red-500" />
                <span>Official TMDB Trailer</span>
              </h3>
              {movie.is_official_trailer && (
                <span className="px-3 py-1 bg-red-950/60 border border-red-800 text-red-400 text-xs font-semibold rounded-full flex items-center space-x-1">
                  <Award className="w-3.5 h-3.5" />
                  <span>Verified Official</span>
                </span>
              )}
            </div>
            <div className="aspect-video w-full max-w-4xl bg-[#141824] rounded-2xl overflow-hidden border border-gray-800 shadow-2xl">
              <iframe 
                src={movie.trailer_url}
                title={`${movie.title} Official Trailer`}
                className="w-full h-full"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          </div>
        ) : (
          <div className="p-6 bg-[#141824] rounded-2xl border border-gray-800 text-center space-y-2 max-w-4xl">
            <VideoOff className="w-8 h-8 text-gray-600 mx-auto" />
            <h4 className="text-sm font-semibold text-gray-300">Official Trailer Unavailable for this Title</h4>
            <p className="text-xs text-gray-500">TMDB metadata does not list an official trailer for "{movie.title}". The movie catalog entry remains fully accessible.</p>
          </div>
        )}
      </div>
    </div>
  );
}
