import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useProfile } from '../context/ProfileContext';
import { Check, Globe, Film, Star, ArrowRight, UserCheck } from 'lucide-react';
import api from '../services/api';

const LANGUAGES = ["Telugu", "Hindi", "Tamil", "Malayalam", "Kannada", "English"];

const GENRES_WITH_VISUALS = [
  { name: "Action", image: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=400&q=80" },
  { name: "Comedy", image: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=400&q=80" },
  { name: "Drama", image: "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=400&q=80" },
  { name: "Crime", image: "https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?auto=format&fit=crop&w=400&q=80" },
  { name: "Thriller", image: "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=400&q=80" },
  { name: "Sci-Fi", image: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=400&q=80" },
  { name: "Romance", image: "https://images.unsplash.com/photo-1518199266791-5375a83190b7?auto=format&fit=crop&w=400&q=80" },
  { name: "Adventure", image: "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=400&q=80" },
  { name: "Horror", image: "https://images.unsplash.com/photo-1509248961158-e54f6934749c?auto=format&fit=crop&w=400&q=80" },
  { name: "Historical", image: "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=400&q=80" }
];

const ACTORS_BY_INDUSTRY = {
  Telugu: [
    { id: 101, name: "Pawan Kalyan" },
    { id: 102, name: "Mahesh Babu" },
    { id: 103, name: "Prabhas" },
    { id: 104, name: "Allu Arjun" },
    { id: 105, name: "Ram Charan" },
    { id: 106, name: "Jr. NTR" },
    { id: 107, name: "Vijay Deverakonda" },
    { id: 108, name: "Nani" },
    { id: 109, name: "Samantha Ruth Prabhu" },
    { id: 110, name: "Rashmika Mandanna" },
    { id: 111, name: "Anushka Shetty" }
  ],
  Hindi: [
    { id: 201, name: "Shah Rukh Khan" },
    { id: 202, name: "Salman Khan" },
    { id: 203, name: "Aamir Khan" },
    { id: 204, name: "Ranbir Kapoor" },
    { id: 205, name: "Ranveer Singh" },
    { id: 206, name: "Alia Bhatt" },
    { id: 207, name: "Deepika Padukone" },
    { id: 208, name: "Rajkummar Rao" }
  ],
  Tamil: [
    { id: 301, name: "Rajinikanth" },
    { id: 302, name: "Kamal Haasan" },
    { id: 303, name: "Thalapathy Vijay" },
    { id: 304, name: "Ajith Kumar" },
    { id: 305, name: "Suriya" },
    { id: 306, name: "Dhanush" },
    { id: 307, name: "Nayanthara" },
    { id: 308, name: "Trisha Krishnan" }
  ],
  Malayalam: [
    { id: 401, name: "Mohanlal" },
    { id: 402, name: "Mammootty" },
    { id: 403, name: "Dulquer Salmaan" },
    { id: 404, name: "Fahadh Faasil" },
    { id: 405, name: "Prithviraj Sukumaran" },
    { id: 406, name: "Nivin Pauly" }
  ],
  Kannada: [
    { id: 501, name: "Yash" },
    { id: 502, name: "Rishab Shetty" },
    { id: 503, name: "Kichcha Sudeep" },
    { id: 504, name: "Darshan" },
    { id: 505, name: "Puneeth Rajkumar" }
  ],
  English: [
    { id: 601, name: "Cillian Murphy" },
    { id: 602, name: "Timothée Chalamet" },
    { id: 603, name: "Tom Cruise" },
    { id: 604, name: "Robert Downey Jr." },
    { id: 605, name: "Zendaya" },
    { id: 606, name: "Margot Robbie" }
  ]
};

export default function Onboarding() {
  const navigate = useNavigate();
  const { user, updateUserState } = useAuth();
  const { selectProfile } = useProfile();

  const [step, setStep] = useState(1);
  const [selectedLanguage, setSelectedLanguage] = useState("Telugu");
  const [selectedGenres, setSelectedGenres] = useState(["Action", "Drama"]);
  const [selectedActorIds, setSelectedActorIds] = useState([]);
  const [loading, setLoading] = useState(false);

  const currentActors = ACTORS_BY_INDUSTRY[selectedLanguage] || ACTORS_BY_INDUSTRY["Telugu"];

  const toggleGenre = (genreName) => {
    if (selectedGenres.includes(genreName)) {
      setSelectedGenres(selectedGenres.filter((g) => g !== genreName));
    } else {
      setSelectedGenres([...selectedGenres, genreName]);
    }
  };

  const toggleActor = (actorId) => {
    if (selectedActorIds.includes(actorId)) {
      setSelectedActorIds(selectedActorIds.filter((id) => id !== actorId));
    } else {
      if (selectedActorIds.length < 5) {
        setSelectedActorIds([...selectedActorIds, actorId]);
      }
    }
  };

  const handleFinish = async () => {
    setLoading(true);
    try {
      // 1. Save Onboarding Preferences
      const onboardingRes = await api.post('/users/onboarding', {
        preferred_language: selectedLanguage,
        favourite_genre_names: selectedGenres,
        favourite_actor_ids: selectedActorIds
      });

      // 2. Save User Profile
      let profileData = { profile_name: user?.name || "My Profile" };
      try {
        const profileRes = await api.post('/users/profiles', profileData);
        selectProfile(profileRes.data);
      } catch (pErr) {
        selectProfile(profileData);
      }

      updateUserState(onboardingRes.data);
      navigate('/home');
    } catch (err) {
      console.error("Failed to complete onboarding:", err);
      navigate('/home');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white flex flex-col justify-between p-6 max-w-4xl mx-auto">
      {/* Header & Step Indicator */}
      <div>
        <div className="flex items-center justify-between py-4 border-b border-gray-800 mb-6">
          <div className="flex items-center space-x-2">
            <Film className="w-6 h-6 text-red-600" />
            <span className="text-xl font-black text-red-600 tracking-wider">Cine<span className="text-white">Nest</span></span>
          </div>
          <div className="text-xs font-semibold text-gray-400">
            Step <span className="text-red-500 font-bold">{step}</span> of 3
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden mb-8">
          <div 
            className="bg-gradient-to-r from-red-600 to-red-500 h-full transition-all duration-300"
            style={{ width: `${(step / 3) * 100}%` }}
          />
        </div>

        {/* STEP 1: Language Selection */}
        {step === 1 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-extrabold mb-2">Select Preferred Language</h2>
              <p className="text-xs text-gray-400">Choose your primary audio language for recommendations.</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {LANGUAGES.map((lang) => {
                const isSelected = selectedLanguage === lang;
                return (
                  <button
                    key={lang}
                    onClick={() => setSelectedLanguage(lang)}
                    className={`p-4 rounded-xl border text-left transition flex items-center justify-between ${
                      isSelected 
                        ? 'bg-red-950/60 border-red-500 text-white font-bold shadow-lg shadow-red-950/30' 
                        : 'bg-[#141824] border-gray-800 text-gray-300 hover:border-gray-600'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <Globe className={`w-5 h-5 ${isSelected ? 'text-red-500' : 'text-gray-400'}`} />
                      <span className="text-sm">{lang}</span>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-red-500" />}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* STEP 2: Visual Genre Selection */}
        {step === 2 && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-extrabold mb-2">Choose Favourite Genres</h2>
              <p className="text-xs text-gray-400">Select 2 or more genres you enjoy watching.</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3.5">
              {GENRES_WITH_VISUALS.map((g) => {
                const isSelected = selectedGenres.includes(g.name);
                return (
                  <button
                    key={g.name}
                    onClick={() => toggleGenre(g.name)}
                    className={`relative h-28 rounded-xl overflow-hidden border-2 text-left p-3 transition transform hover:scale-102 ${
                      isSelected ? 'border-red-500 ring-2 ring-red-500/50' : 'border-gray-800 hover:border-gray-600'
                    }`}
                  >
                    <img src={g.image} alt={g.name} className="absolute inset-0 w-full h-full object-cover filter brightness-50" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent" />
                    <div className="relative z-10 flex flex-col justify-between h-full">
                      <span className="text-xs font-black tracking-wider text-white uppercase">{g.name}</span>
                      {isSelected && (
                        <span className="self-end p-1 bg-red-600 rounded-full text-white">
                          <Check className="w-3 h-3" />
                        </span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* STEP 3: Industry-Based Actor Selection */}
        {step === 3 && (
          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-1">
                <h2 className="text-2xl sm:text-3xl font-extrabold">Pick Favourite Actors ({selectedLanguage})</h2>
                <span className="text-xs text-red-400 font-bold">{selectedActorIds.length}/5 Selected</span>
              </div>
              <p className="text-xs text-gray-400">Showing top actors and actresses for <strong>{selectedLanguage}</strong> cinema.</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
              {currentActors.map((actor) => {
                const isSelected = selectedActorIds.includes(actor.id);
                return (
                  <button
                    key={actor.id}
                    onClick={() => toggleActor(actor.id)}
                    className={`p-3.5 rounded-xl border text-center transition flex items-center justify-between space-x-2 ${
                      isSelected 
                        ? 'bg-red-950/60 border-red-500 text-white font-bold shadow-lg shadow-red-950/30' 
                        : 'bg-[#141824] border-gray-800 text-gray-300 hover:border-gray-600'
                    }`}
                  >
                    <div className="flex items-center space-x-2 truncate">
                      <Star className={`w-4 h-4 flex-shrink-0 ${isSelected ? 'text-amber-400 fill-current' : 'text-gray-500'}`} />
                      <span className="text-xs truncate">{actor.name}</span>
                    </div>
                    {isSelected && <Check className="w-3.5 h-3.5 text-red-400 flex-shrink-0" />}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Footer Navigation */}
      <div className="flex items-center justify-between py-4 border-t border-gray-800">
        {step > 1 ? (
          <button
            onClick={() => setStep(step - 1)}
            className="px-5 py-2.5 bg-gray-800 text-gray-300 text-xs font-semibold rounded-lg hover:bg-gray-700"
          >
            Back
          </button>
        ) : <div />}

        {step < 3 ? (
          <button
            onClick={() => setStep(step + 1)}
            className="px-6 py-2.5 bg-red-600 text-white text-xs font-bold rounded-lg hover:bg-red-700 flex items-center space-x-2 shadow-lg shadow-red-950/40"
          >
            <span>Next</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        ) : (
          <button
            onClick={handleFinish}
            disabled={loading}
            className="px-6 py-2.5 bg-red-600 text-white text-xs font-bold rounded-lg hover:bg-red-700 flex items-center space-x-2 shadow-lg shadow-red-950/50"
          >
            <UserCheck className="w-4 h-4" />
            <span>{loading ? 'Completing Setup...' : 'Complete & Start Watching'}</span>
          </button>
        )}
      </div>
    </div>
  );
}
