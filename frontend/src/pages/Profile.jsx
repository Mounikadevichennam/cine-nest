import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import { useProfile } from '../context/ProfileContext';
import { User, Mail, Globe, ShieldAlert, Check } from 'lucide-react';
import api from '../services/api';

export default function Profile() {
  const { user, updateUserState, isAdmin } = useAuth();
  const { activeProfile } = useProfile();
  const [preferredLanguage, setPreferredLanguage] = useState(user?.preferred_language || 'Telugu');
  const [saved, setSaved] = useState(false);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/users/onboarding', {
        preferred_language: preferredLanguage,
        favourite_genre_ids: [],
        favourite_actor_ids: []
      });
      updateUserState(res.data);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error("Failed to update profile preferences:", err);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0D12] text-white pt-24 pb-20">
      <Navbar />

      <div className="max-w-3xl mx-auto px-6 space-y-6">
        <h1 className="text-3xl font-extrabold">Account & Profile Settings</h1>

        <div className="bg-[#141824] p-8 rounded-2xl border border-gray-800 space-y-6 shadow-xl">
          {/* Active Profile Info */}
          <div className="flex items-center space-x-4 pb-6 border-b border-gray-800">
            <img 
              src={activeProfile?.avatar || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"} 
              alt="Avatar" 
              className="w-16 h-16 rounded-xl object-cover border-2 border-red-600 shadow-lg"
            />
            <div>
              <h3 className="text-xl font-bold text-white">{activeProfile?.profile_name || user?.name}</h3>
              <p className="text-xs text-gray-400 mt-0.5">Active Watching Profile</p>
            </div>
          </div>

          {/* Account Details Form */}
          <form onSubmit={handleSave} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-400 mb-1">Full Name</label>
              <div className="relative">
                <User className="absolute left-3.5 top-3 w-4 h-4 text-gray-500" />
                <input 
                  type="text" 
                  disabled
                  value={user?.name || ''}
                  className="w-full pl-10 pr-4 py-2.5 bg-[#0B0D12] border border-gray-800 rounded-lg text-sm text-gray-400 cursor-not-allowed"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-400 mb-1">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-3 w-4 h-4 text-gray-500" />
                <input 
                  type="email" 
                  disabled
                  value={user?.email || ''}
                  className="w-full pl-10 pr-4 py-2.5 bg-[#0B0D12] border border-gray-800 rounded-lg text-sm text-gray-400 cursor-not-allowed"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 mb-1">Preferred Language Signal</label>
              <div className="relative">
                <Globe className="absolute left-3.5 top-3 w-4 h-4 text-gray-500" />
                <select
                  value={preferredLanguage}
                  onChange={(e) => setPreferredLanguage(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-[#0B0D12] border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:border-red-500"
                >
                  <option value="Telugu">Telugu</option>
                  <option value="Hindi">Hindi</option>
                  <option value="Tamil">Tamil</option>
                  <option value="Malayalam">Malayalam</option>
                  <option value="Kannada">Kannada</option>
                  <option value="English">English</option>
                </select>
              </div>
            </div>

            {isAdmin && (
              <div className="p-4 bg-red-950/30 border border-red-800/40 rounded-xl flex items-center space-x-3 text-red-400 text-xs">
                <ShieldAlert className="w-5 h-5 flex-shrink-0" />
                <span>You are logged in as an <strong>Administrator</strong> (`ADMIN` role). You have access to catalog management CRUD tools.</span>
              </div>
            )}

            <div className="flex items-center justify-between pt-4 border-t border-gray-800">
              {saved ? (
                <span className="text-xs text-green-400 font-semibold flex items-center space-x-1">
                  <Check className="w-4 h-4" />
                  <span>Preferences saved successfully!</span>
                </span>
              ) : <div />}

              <button
                type="submit"
                className="px-6 py-2.5 bg-red-600 text-white text-xs font-bold rounded-lg hover:bg-red-700 transition shadow-lg shadow-red-950/50"
              >
                Save Preferences
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
