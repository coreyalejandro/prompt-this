import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Profile = () => {
  const { user, isAuthenticated } = useAuth();
  const [profile, setProfile] = useState({ points: 0, achievements: [] });

  useEffect(() => {
    const fetchProfile = async () => {
      if (!user) return;
      try {
        const res = await axios.get(`${API}/users/${user.id}/profile`);
        setProfile(res.data);
      } catch (err) {
        console.error('Error fetching profile:', err);
      }
    };
    fetchProfile();
  }, [user]);

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p>Please sign in to view your profile.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Profile</h1>
      <p className="mb-4">Points: {profile.points}</p>
      <h2 className="text-2xl font-semibold mb-2">Achievements</h2>
      <div className="flex space-x-4">
        {profile.achievements.length > 0 ? (
          profile.achievements.map((ach, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl">{ach.icon}</div>
              <div className="text-sm mt-1">{ach.name}</div>
            </div>
          ))
        ) : (
          <p>No achievements yet.</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
