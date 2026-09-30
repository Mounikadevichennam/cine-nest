import React, { createContext, useContext, useState, useEffect } from 'react';

const ProfileContext = createContext();

export const ProfileProvider = ({ children }) => {
  const [activeProfile, setActiveProfile] = useState(() => {
    const saved = localStorage.getItem('cinenest_profile');
    return saved ? JSON.parse(saved) : null;
  });

  const selectProfile = (profile) => {
    setActiveProfile(profile);
    localStorage.setItem('cinenest_profile', JSON.stringify(profile));
  };

  return (
    <ProfileContext.Provider value={{ activeProfile, selectProfile }}>
      {children}
    </ProfileContext.Provider>
  );
};

export const useProfile = () => useContext(ProfileContext);
