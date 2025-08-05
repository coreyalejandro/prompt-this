
import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const LoginModal = ({ isOpen, onClose }) => {
  const [username, setUsername] = useState('');
  const { login } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) {
      login(username.trim());
      onClose();
    }
  };

  const handleQuickLogin = () => {
    login(); // Uses 'Anonymous User' as default
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="glass rounded-lg shadow-xl max-w-md w-full p-4 sm:p-6">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4">Welcome to Prompt-This!</h2>
        <p className="text-base sm:text-base text-gray-600 mb-6">
          To save your workflows and track your progress, please choose how you'd like to continue:
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Username (Optional)
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-2 sm:p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your name..."
            />
          </div>

          <div className="space-y-3">
            <button
              type="submit"
              disabled={!username.trim()}
              className="w-full bg-blue-500 text-white py-2 sm:py-3 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              Continue as "{username || 'Your Name'}"
            </button>

            <button
              type="button"
              onClick={handleQuickLogin}
              className="w-full bg-gray-500 text-white py-2 sm:py-3 px-4 rounded-lg hover:bg-gray-600 transition-colors"
            >
              Continue as Guest
            </button>
          </div>
        </form>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-medium text-blue-800 mb-2">Why sign in?</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Save your custom workflows</li>
            <li>• Track your agent usage</li>
            <li>• Access your workflow history</li>
            <li>• Resume where you left off</li>
          </ul>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-gray-500">
            No account required • Data stored locally • Privacy-first approach
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;
