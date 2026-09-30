import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import HeroBanner from '../components/HeroBanner';
import MovieRow from '../components/MovieRow';
import { recommendationService } from '../services/recommendationService';
import api from '../services/api';
import { Sparkles, Flame, Film, Clock, Heart, Star, Compass } from 'lucide-react';

export default function Home() {
  const [heroMovie, setHeroMovie] = useState(null);
  const [recommended, setRecommended] = useState([]);
  const [trending, setTrending] = useState([]);
  const [newReleases, setNewReleases] = useState([]);
  const [becauseWatched, setBecauseWatched] = useState([]);
  const [byGenres, setByGenres] = useState([]);
  const [byActors, setByActors] = useState([]);
  const [continueWatching, setContinueWatching] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAllFeeds = async () => {
      setLoading(true);
      try {
        const results = await Promise.allSettled([
          recommendationService.getRecommendedForYou(),
          recommendationService.getTrending(),
          recommendationService.getNewReleases(),
          recommendationService.getBecauseYouWatched(),
          recommendationService.getByGenres(),
          recommendationService.getByActors(),
          recommendationService.getContinueWatching(),
        ]);

        const recData = results[0].status === 'fulfilled' ? results[0].value : [];
        const trendData = results[1].status === 'fulfilled' ? results[1].value : [];
        const newData = results[2].status === 'fulfilled' ? results[2].value : [];
        const becData = results[3].status === 'fulfilled' ? results[3].value : [];
        const genreData = results[4].status === 'fulfilled' ? results[4].value : [];
        const actorData = results[5].status === 'fulfilled' ? results[5].value : [];
        const cwData = results[6].status === 'fulfilled' ? results[6].value : [];

        // General fallback from main movie catalog if specific feeds are empty
        let generalCatalog = [];
        if (!recData.length || !trendData.length || !newData.length) {
          try {
            const catRes = await api.get('/movies?limit=30');
            generalCatalog = catRes.data || [];
          } catch (catErr) {
            console.error("Failed to load catalog fallback:", catErr);
          }
        }

        const finalRec = recData.length > 0 ? recData : generalCatalog;
        const finalTrend = trendData.length > 0 ? trendData : generalCatalog;
        const finalNew = newData.length > 0 ? newData : generalCatalog.filter(m => m.release_year >= 2024);
        const finalGenre = genreData.length > 0 ? genreData : generalCatalog;
        const finalActor = actorData.length > 0 ? actorData : generalCatalog;

        setRecommended(finalRec);
        setTrending(finalTrend);
        setNewReleases(finalNew);
        setBecauseWatched(becData);
        setByGenres(finalGenre);
        setByActors(finalActor);
        setContinueWatching(cwData);

        // Set Hero Movie
        if (finalRec && finalRec.length > 0) {
          setHeroMovie(finalRec[0]);
        } else if (finalTrend && finalTrend.length > 0) {
          setHeroMovie(finalTrend[0]);
        } else if (generalCatalog.length > 0) {
          setHeroMovie(generalCatalog[0]);
        }
      } catch (err) {
        console.error("Failed to load recommendation feeds:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllFeeds();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B0D12] flex flex-col items-center justify-center text-white">
        <div className="w-12 h-12 border-4 border-red-600 border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-xs text-gray-400 font-mono">Loading CineNest Recommendation Feeds...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white pb-20">
      {/* Top Navigation */}
      <Navbar />

      {/* Hero Banner */}
      {heroMovie && <HeroBanner movie={heroMovie} />}

      {/* Movie Rows */}
      <div className="max-w-7xl mx-auto space-y-6 pt-4">
        {/* Continue Watching */}
        {continueWatching.length > 0 && (
          <MovieRow title="Continue Watching" movies={continueWatching} icon={Clock} />
        )}

        {/* Recommended For You (AI Hybrid Model) */}
        {recommended.length > 0 && (
          <MovieRow title="Recommended For You" movies={recommended} icon={Sparkles} />
        )}

        {/* Trending Now */}
        {trending.length > 0 && (
          <MovieRow title="Trending Now" movies={trending} icon={Flame} />
        )}

        {/* New Releases (2024-2026) */}
        {newReleases.length > 0 && (
          <MovieRow title="New Releases" movies={newReleases} icon={Film} />
        )}

        {/* Because You Watched */}
        {becauseWatched.length > 0 && (
          <MovieRow title="Because You Watched" movies={becauseWatched} icon={Compass} />
        )}

        {/* Based on Favourite Genres */}
        {byGenres.length > 0 && (
          <MovieRow title="Based on Your Favourite Genres" movies={byGenres} icon={Heart} />
        )}

        {/* Based on Favourite Actors */}
        {byActors.length > 0 && (
          <MovieRow title="Based on Your Favourite Actors" movies={byActors} icon={Star} />
        )}
      </div>
    </div>
  );
}
