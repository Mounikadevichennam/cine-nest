import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ProfileProvider } from './context/ProfileContext';

// Pages
import Login from './pages/Login';
import Signup from './pages/Signup';
import WhoIsWatching from './pages/WhoIsWatching';
import Onboarding from './pages/Onboarding';
import Home from './pages/Home';
import Browse from './pages/Browse';
import Search from './pages/Search';
import MovieDetails from './pages/MovieDetails';
import Watch from './pages/Watch';
import Profile from './pages/Profile';

// Admin Pages
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';
import MovieManagement from './pages/admin/MovieManagement';
import AddMovie from './pages/admin/AddMovie';
import EditMovie from './pages/admin/EditMovie';

// Protected Route for Logged In Subscribers
const UserProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <div className="min-h-screen bg-[#0B0D12]" />;
  if (!user) return <Navigate to="/login" replace />;
  return children;
};

// Protected Route Exclusively for Admins
const AdminProtectedRoute = ({ children }) => {
  const { user, loading, isAdmin } = useAuth();
  if (loading) return <div className="min-h-screen bg-[#0B0D12]" />;
  if (!user) return <Navigate to="/admin/login" replace />;
  if (!isAdmin) return <Navigate to="/home" replace />;
  return children;
};

export default function App() {
  return (
    <AuthProvider>
      <ProfileProvider>
        <Router>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/admin/login" element={<AdminLogin />} />

            {/* Subscriber Protected Routes */}
            <Route path="/who-is-watching" element={<UserProtectedRoute><WhoIsWatching /></UserProtectedRoute>} />
            <Route path="/onboarding" element={<UserProtectedRoute><Onboarding /></UserProtectedRoute>} />
            <Route path="/home" element={<UserProtectedRoute><Home /></UserProtectedRoute>} />
            <Route path="/browse" element={<UserProtectedRoute><Browse /></UserProtectedRoute>} />
            <Route path="/search" element={<UserProtectedRoute><Search /></UserProtectedRoute>} />
            <Route path="/movie/:id" element={<UserProtectedRoute><MovieDetails /></UserProtectedRoute>} />
            <Route path="/watch/:id" element={<UserProtectedRoute><Watch /></UserProtectedRoute>} />
            <Route path="/profile" element={<UserProtectedRoute><Profile /></UserProtectedRoute>} />

            {/* Admin Protected Routes */}
            <Route path="/admin/dashboard" element={<AdminProtectedRoute><AdminDashboard /></AdminProtectedRoute>} />
            <Route path="/admin/movies" element={<AdminProtectedRoute><MovieManagement /></AdminProtectedRoute>} />
            <Route path="/admin/movies/add" element={<AdminProtectedRoute><AddMovie /></AdminProtectedRoute>} />
            <Route path="/admin/movies/edit/:id" element={<AdminProtectedRoute><EditMovie /></AdminProtectedRoute>} />

            {/* Fallback Catch-all Route */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Router>
      </ProfileProvider>
    </AuthProvider>
  );
}
