import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              Aakaar Project
            </Link>
          </div>
          <div className="hidden md:flex space-x-4">
            <Link to="/dashboard" className="hover:text-gray-300">
              Dashboard
            </Link>
            <Link to="/files" className="hover:text-gray-300">
              Files
            </Link>
            <Link to="/ai" className="hover:text-gray-300">
              AI
            </Link>
            <Link to="/clients" className="hover:text-gray-300">
              Clients
            </Link>
            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="hover:text-gray-300"
              >
                Logout
              </button>
            )}
          </div>
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!isMobileMenuOpen)}
              className="text-gray-300 hover:text-white focus:outline-none"
            >
              ☰
            </button>
          </div>
        </div>
      </div>
      {isMobileMenuOpen && (
        <div className="md:hidden bg-gray-700">
          <Link to="/dashboard" className="block px-4 py-2 hover:bg-gray-600">
            Dashboard
          </Link>
          <Link to="/files" className="block px-4 py-2 hover:bg-gray-600">
            Files
          </Link>
          <Link to="/ai" className="block px-4 py-2 hover:bg-gray-600">
            AI
          </Link>
          <Link to="/clients" className="block px-4 py-2 hover:bg-gray-600">
            Clients
          </Link>
          {isAuthenticated && (
            <button
              onClick={handleLogout}
              className="block w-full text-left px-4 py-2 hover:bg-gray-600"
            >
              Logout
            </button>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;