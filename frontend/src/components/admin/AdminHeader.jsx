import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck } from 'lucide-react';

export default function AdminHeader({ title }) {
  const { user } = useAuth();

  return (
    <header className="h-16 bg-[#141824] border-b border-gray-800 px-8 flex items-center justify-between">
      <h1 className="text-lg font-bold text-white tracking-wide">{title}</h1>

      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-1.5 px-3 py-1 bg-red-950/60 border border-red-800/60 rounded-full text-[11px] font-bold text-red-400">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>ADMIN ROLE AUTHORIZED</span>
        </div>
        <span className="text-xs text-gray-300 font-medium">{user?.name}</span>
      </div>
    </header>
  );
}
