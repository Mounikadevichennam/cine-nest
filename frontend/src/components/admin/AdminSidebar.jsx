import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Film, LayoutDashboard, Film as MovieIcon, PlusCircle, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function AdminSidebar() {
  const location = useLocation();
  const { logout } = useAuth();

  const isActive = (path) => location.pathname === path;

  return (
    <aside className="w-64 bg-[#141824] border-r border-gray-800 p-6 min-h-screen flex flex-col justify-between">
      <div className="space-y-8">
        {/* Brand */}
        <Link to="/home" className="flex items-center space-x-2 text-xl font-black text-red-600">
          <Film className="w-6 h-6 text-red-600" />
          <span>Cine<span className="text-white">Nest Admin</span></span>
        </Link>

        {/* Links */}
        <nav className="space-y-2 text-xs font-semibold text-gray-400">
          <Link 
            to="/admin/dashboard" 
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
              isActive('/admin/dashboard') 
                ? 'bg-red-600 text-white font-bold shadow-lg shadow-red-950/40' 
                : 'hover:bg-gray-800/60 hover:text-white'
            }`}
          >
            <LayoutDashboard className="w-4 h-4" />
            <span>Dashboard</span>
          </Link>

          <Link 
            to="/admin/movies" 
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
              isActive('/admin/movies') 
                ? 'bg-red-600 text-white font-bold shadow-lg shadow-red-950/40' 
                : 'hover:bg-gray-800/60 hover:text-white'
            }`}
          >
            <MovieIcon className="w-4 h-4" />
            <span>Movie Catalog</span>
          </Link>

          <Link 
            to="/admin/movies/add" 
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
              isActive('/admin/movies/add') 
                ? 'bg-red-600 text-white font-bold shadow-lg shadow-red-950/40' 
                : 'hover:bg-gray-800/60 hover:text-white'
            }`}
          >
            <PlusCircle className="w-4 h-4" />
            <span>Add Movie</span>
          </Link>
        </nav>
      </div>

      <div className="pt-6 border-t border-gray-800">
        <Link 
          to="/home" 
          className="w-full flex items-center space-x-2 text-xs text-gray-400 hover:text-white px-4 py-2 hover:bg-gray-800/50 rounded-lg transition"
        >
          <LogOut className="w-4 h-4" />
          <span>Return to User App</span>
        </Link>
      </div>
    </aside>
  );
}
