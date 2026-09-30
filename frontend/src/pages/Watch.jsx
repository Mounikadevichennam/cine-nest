import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { movieService } from '../services/movieService';
import { ArrowLeft, Play, Pause, Volume2, VolumeX, Maximize, Film, Info, ShieldCheck } from 'lucide-react';

export default function Watch() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const mode = searchParams.get('mode') || 'movie'; // 'movie' or 'trailer'
  const navigate = useNavigate();

  const [movie, setMovie] = useState(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(15);
  const [duration, setDuration] = useState(120);
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
          <span className={`px-3 py-1 rounded-full text-[11px] font-bold border flex items-center space-x-1 ${
            mode === 'trailer' 
              ? 'bg-amber-950/70 border-amber-500 text-amber-300' 
              : 'bg-red-950/70 border-red-500 text-red-300'
          }`}>
            {mode === 'trailer' ? <Film className="w-3.5 h-3.5" /> : <ShieldCheck className="w-3.5 h-3.5" />}
            <span>{mode === 'trailer' ? 'Official TMDB Trailer' : 'CineNest Feature Stream (Demo)'}</span>
          </span>
        </div>
      </div>

      {/* Main Video Viewport */}
      <div className="relative w-full h-screen flex items-center justify-center bg-black">
        {mode === 'trailer' && movie?.trailer_url ? (
          <iframe 
            src={`${movie.trailer_url}?autoplay=1&mute=${isMuted ? 1 : 0}`} 
            title={`${movie.title} Trailer`}
            className="w-full h-full border-0 pointer-events-auto"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <div className="text-center space-y-4 max-w-lg p-8 bg-[#141824] rounded-2xl border border-gray-800 shadow-2xl relative z-20">
            <div className="w-16 h-16 rounded-full bg-red-600/20 text-red-500 flex items-center justify-center mx-auto shadow-inner">
              <Play className="w-8 h-8 fill-current ml-1" />
            </div>
            <div>
              <h3 className="text-xl font-extrabold text-white mb-1">{movie?.title}</h3>
              <p className="text-xs text-red-400 font-semibold">CineNest Academic Prototype Feature Stream</p>
            </div>
            
            <div className="p-3 bg-gray-900/80 rounded-lg text-left space-y-1.5 border border-gray-800">
              <div className="flex items-center space-x-1.5 text-gray-300 text-xs font-bold">
                <Info className="w-4 h-4 text-amber-400 flex-shrink-0" />
                <span>Notice on Content Streaming:</span>
              </div>
              <p className="text-[11px] text-gray-400 leading-normal">
                TMDB provides official metadata and trailers. For copyrighted full feature films, this academic prototype simulates live OTT playback progress, tracking completion %, watch history, and activity signals into the CineNest recommendation engine.
              </p>
            </div>
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
