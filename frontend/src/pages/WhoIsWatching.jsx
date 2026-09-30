import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useProfile } from '../context/ProfileContext';
import { User, Smile, Users } from 'lucide-react';
import api from '../services/api';

export default function WhoIsWatching() {
  const { user } = useAuth();
  const { selectProfile } = useProfile();
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);

  useEffect(() => {
    const fetchProfiles = async () => {
      let userName = user?.name || "User";
      try {
        const res = await api.get('/users/profiles');
        const dbProfiles = res.data || [];
        if (dbProfiles.length > 0) {
          userName = dbProfiles[0].profile_name || userName;
        }
      } catch (err) {
        // Fallback
      }

      setProfiles([
        { id: 1, profile_name: userName, type: 'user', bg: 'from-red-600 to-red-900', icon: User },
        { id: 2, profile_name: "Kids", type: 'kids', bg: 'from-amber-500 to-amber-800', icon: Smile },
        { id: 3, profile_name: "Others", type: 'others', bg: 'from-indigo-600 to-indigo-900', icon: Users }
      ]);
    };
    fetchProfiles();
  }, [user]);

  const handleSelect = (profile) => {
    selectProfile(profile);
    navigate('/home');
  };

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl sm:text-5xl font-black mb-12 tracking-tight">Who is watching?</h1>

      <div className="flex flex-wrap items-center justify-center gap-8 max-w-4xl">
        {profiles.map((profile) => {
          const IconComponent = profile.icon;
          return (
            <button
              key={profile.id}
              onClick={() => handleSelect(profile)}
              className="group flex flex-col items-center space-y-3 focus:outline-none"
            >
              <div className={`relative w-28 h-28 sm:w-36 sm:h-36 rounded-2xl bg-gradient-to-br ${profile.bg} flex items-center justify-center border-2 border-transparent group-hover:border-white transition transform group-hover:scale-105 shadow-2xl`}>
                <IconComponent className="w-14 h-14 text-white drop-shadow-md" />
              </div>
              <span className="text-base font-bold text-gray-300 group-hover:text-white transition">
                {profile.profile_name}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
