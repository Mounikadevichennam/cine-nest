import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useProfile } from '../context/ProfileContext';
import { Film, Search, User, LogOut, ShieldAlert, Sliders } from 'lucide-react';

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth();
  const { activeProfile } = useProfile();
  const navigate = useNavigate();
  const location = useLocation();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0B0D12]/90 backdrop-blur-md border-b border-gray-800/60 px-6 py-3.5 flex items-center justify-between transition-all">
      {/* Brand Identity */}
      <div className="flex items-center space-x-8">
        <Link to="/home" className="flex items-center space-x-2 text-2xl font-black tracking-wider text-red-600">
          <Film className="w-7 h-7 text-red-600" />
          <span>Cine<span className="text-white font-bold">Nest</span></span>
        </Link>

        {/* Primary Links */}
        <div className="hidden md:flex items-center space-x-6 text-sm font-medium">
          <Link to="/home" className={`${isActive('/home') ? 'text-white font-semibold' : 'text-gray-400 hover:text-gray-200'} transition`}>
            Home
          </Link>
          <Link to="/browse" className={`${isActive('/browse') ? 'text-white font-semibold' : 'text-gray-400 hover:text-gray-200'} transition`}>
            Browse
          </Link>
          <Link to="/search" className={`${isActive('/search') ? 'text-white font-semibold' : 'text-gray-400 hover:text-gray-200'} transition flex items-center space-x-1`}>
            <Search className="w-4 h-4" />
            <span>Search</span>
          </Link>
        </div>
      </div>

      {/* Profile & Controls */}
      <div className="flex items-center space-x-4">
        {/* Search quick button mobile */}
        <Link to="/search" className="md:hidden text-gray-400 hover:text-white p-2">
          <Search className="w-5 h-5" />
        </Link>

        {/* Admin Portal Badge */}
        {isAdmin && (
          <Link to="/admin/dashboard" className="hidden sm:flex items-center space-x-1.5 px-3 py-1 bg-red-950/60 border border-red-800/60 text-red-400 text-xs font-semibold rounded-full hover:bg-red-900/80 transition">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Admin Portal</span>
          </Link>
        )}

        {/* Profile Avatar Dropdown */}
        <div className="relative">
          <button 
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-2.5 focus:outline-none group"
          >
            <div className="w-8 h-8 rounded-md bg-gradient-to-br from-red-600 to-red-900 flex items-center justify-center text-xs font-black text-white border border-gray-700 group-hover:border-red-500 transition shadow-sm">
              {(activeProfile?.profile_name || user?.name || "U")[0].toUpperCase()}
            </div>
            <span className="hidden md:inline text-xs font-medium text-gray-300 group-hover:text-white">
              {activeProfile?.profile_name || user?.name}
            </span>
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-[#141824] border border-gray-800 rounded-lg shadow-xl py-2 z-50 text-xs text-gray-300">
              <div className="px-4 py-2 border-b border-gray-800">
                <p className="font-semibold text-white">{user?.name}</p>
                <p className="text-gray-500 truncate">{user?.email}</p>
              </div>
              
              <Link 
                to="/who-is-watching" 
                onClick={() => setDropdownOpen(false)} 
                className="flex items-center space-x-2 px-4 py-2 hover:bg-gray-800/60 text-gray-300 hover:text-white transition"
              >
                <User className="w-4 h-4" />
                <span>Switch Profile</span>
              </Link>

              <Link 
                to="/onboarding" 
                onClick={() => setDropdownOpen(false)} 
                className="flex items-center space-x-2 px-4 py-2 hover:bg-gray-800/60 text-gray-300 hover:text-white transition"
              >
                <Sliders className="w-4 h-4" />
                <span>Preferences</span>
              </Link>

              {isAdmin && (
                <Link 
                  to="/admin/dashboard" 
                  onClick={() => setDropdownOpen(false)} 
                  className="flex items-center space-x-2 px-4 py-2 hover:bg-red-950/40 text-red-400 font-semibold transition"
                >
                  <ShieldAlert className="w-4 h-4" />
                  <span>Admin Dashboard</span>
                </Link>
              )}

              <button 
                onClick={handleLogout}
                className="w-full text-left flex items-center space-x-2 px-4 py-2 hover:bg-red-950/60 text-red-400 transition border-t border-gray-800/60 mt-1"
              >
                <LogOut className="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
