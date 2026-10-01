import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { movieService } from '../services/movieService';
import { ArrowLeft, Play, Pause, Volume2, VolumeX, Maximize, Film, VideoOff, Star } from 'lucide-react';

export default function Watch() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const mode = searchParams.get('mode') || 'trailer'; // 'trailer' or 'movie'
  const navigate = useNavigate();

  const [movie, setMovie] = useState(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(15);
  const [duration] = useState(120);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const data = await movieService.getMovieDetails(id);
        setMovie(data);
      } catch (err) {
        console.error("Failed to load movie for player:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMovie();
  }, [id]);

  // Periodic watch progress recording to engine
  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(async () => {
      setProgress((prev) => {
        const next = prev + 2;
        const completion = Math.min(100, (next / duration) * 100);
        movieService.recordWatchProgress(id, next, completion).catch(() => {});
        return next;
      });
    }, 3000);

    return () => clearInterval(interval);
  }, [id, isPlaying, duration]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B0D12] flex items-center justify-center text-white font-mono text-xs">
        Initializing Player...
      </div>
    );
  }

  const completionPercentage = Math.round((progress / duration) * 100);
  const hasTrailer = Boolean(movie?.trailer_url);

  return (
    <div className="min-h-screen bg-black text-white flex flex-col justify-between relative overflow-hidden select-none">
      {/* Top Overlay Bar */}
      <div className="absolute top-0 left-0 right-0 z-30 p-6 bg-gradient-to-b from-black/90 to-transparent flex items-center justify-between">
        <button 
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 text-xs font-semibold text-gray-300 hover:text-white transition bg-black/40 px-3.5 py-1.5 rounded-full border border-white/10"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Exit Player</span>
        </button>

        <div className="flex items-center space-x-3">
          <span className="text-sm font-bold text-white tracking-wide">{movie?.title}</span>
          {movie?.release_year && (
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-red-950/70 border border-red-500/50 text-red-300">
              {movie.release_year}
            </span>
          )}
        </div>
      </div>

      {/* Main Video Viewport */}
      <div className="relative w-full h-screen flex items-center justify-center bg-black">
        {hasTrailer ? (
          <iframe 
            src={`${movie.trailer_url}?autoplay=1&mute=${isMuted ? 1 : 0}`} 
            title={`${movie.title} Official Trailer`}
            className="w-full h-full border-0 pointer-events-auto"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <div className="text-center space-y-4 max-w-md p-8 bg-[#141824] rounded-2xl border border-gray-800 shadow-2xl relative z-20">
            <div className="w-16 h-16 rounded-full bg-gray-800 text-gray-400 flex items-center justify-center mx-auto shadow-inner">
              <VideoOff className="w-8 h-8" />
            </div>
            <div>
              <h3 className="text-xl font-extrabold text-white mb-1">{movie?.title || "Movie Player"}</h3>
              <p className="text-xs text-gray-400">Official trailer video is currently unavailable for this title.</p>
            </div>
            <button 
              onClick={() => navigate(-1)}
              className="px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-lg shadow-lg"
            >
              Return to Movie Details
            </button>
          </div>
        )}
      </div>

      {/* Bottom OTT Playbar */}
      <div className="absolute bottom-0 left-0 right-0 z-30 p-6 bg-gradient-to-t from-black/90 via-black/60 to-transparent space-y-3">
        {/* Progress Bar */}
        <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
          <div 
            className="bg-red-600 h-full transition-all duration-300"
            style={{ width: `${completionPercentage}%` }}
          />
        </div>

        {/* Playback Controls */}
        <div className="flex items-center justify-between text-xs text-gray-300">
          <div className="flex items-center space-x-4">
            <button onClick={() => setIsPlaying(!isPlaying)} className="hover:text-white transition">
              {isPlaying ? <Pause className="w-5 h-5 fill-current" /> : <Play className="w-5 h-5 fill-current" />}
            </button>

            <button onClick={() => setIsMuted(!isMuted)} className="hover:text-white transition">
              {isMuted ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
            </button>

            <span className="font-mono text-[11px]">
              {Math.floor(progress / 60)}:{String(progress % 60).padStart(2, '0')} / {Math.floor(duration / 60)}:{String(duration % 60).padStart(2, '0')} ({completionPercentage}%)
            </span>
          </div>

          <button onClick={() => document.documentElement.requestFullscreen?.()} className="hover:text-white transition">
            <Maximize className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
