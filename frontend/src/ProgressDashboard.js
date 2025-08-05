import React from "react";
import { useAuth } from "./AuthContext";

const ProgressDashboard = () => {
  const { progress } = useAuth();
  const exercisesCount = progress?.completedExercises?.length || 0;
  const tutorialsCount = progress?.completedTutorials?.length || 0;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Your Progress</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-2">Tutorials Completed</h2>
          <p className="text-3xl font-bold text-blue-600">{tutorialsCount}</p>
        </div>
        <div className="glass rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-2">Exercises Completed</h2>
          <p className="text-3xl font-bold text-green-600">{exercisesCount}</p>
        </div>
      </div>
    </div>
  );
};

export default ProgressDashboard;
