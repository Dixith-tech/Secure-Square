"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Shield, AlertCircle, Eye, EyeOff } from 'lucide-react';
import API from '@/services/api';
import { getFingerprint } from '@/services/fingerprint';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Get device fingerprint
      let fingerprint = null;
      try {
        fingerprint = await getFingerprint();
      } catch (err) {
        console.warn('Could not get device fingerprint:', err);
      }

      // Send login request
      const response = await API.post('/api/v1/auth/login', {
        email,
        password,
        device_fingerprint: fingerprint
      });

      // Store token
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data.user));

        // Redirect to dashboard
        setTimeout(() => {
          router.push('/dashboard');
        }, 500);
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Login failed. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center mb-8">
          <Shield className="text-blue-500 mr-3" size={40} />
          <div>
            <h1 className="text-3xl font-bold text-white">SecureAI</h1>
            <p className="text-xs text-blue-400">Threat Detection Platform</p>
          </div>
        </div>

        {/* Card */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Security Login</h2>

          {/* Error Message */}
          {error && (
            <div className="bg-red-900/20 border border-red-700 text-red-400 p-4 rounded-lg mb-6 flex items-start gap-3">
              <AlertCircle size={20} className="mt-0.5 flex-shrink-0" />
              <p className="text-sm">{error}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleLogin} className="space-y-5">
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                placeholder="admin@example.com"
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50 transition"
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  placeholder="••••••••"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50 transition pr-10"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-300"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-600 disabled:opacity-50 text-white font-semibold py-3 px-4 rounded-lg transition flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Authenticating...
                </>
              ) : (
                <>
                  <Shield size={20} />
                  Login
                </>
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-6 p-4 bg-gray-800/50 border border-gray-700 rounded-lg">
            <p className="text-xs text-gray-400 font-semibold mb-2">Demo Credentials:</p>
            <p className="text-xs text-gray-500 mb-1">Email: <span className="text-gray-400 font-mono">admin@example.com</span></p>
            <p className="text-xs text-gray-500">Password: <span className="text-gray-400 font-mono">Password1</span></p>
          </div>

          {/* Footer */}
          <div className="mt-6 text-center text-xs text-gray-500">
            <p>SecureAI v1.0.0 | AI-Powered Threat Detection</p>
            <p className="mt-2">
              <a href="#" className="text-blue-400 hover:text-blue-300">
                Privacy Policy
              </a>
              {' '} • {' '}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                Terms
              </a>
            </p>
          </div>
        </div>

        {/* Security Badge */}
        <div className="mt-8 text-center text-xs text-gray-600 flex items-center justify-center gap-2">
          <Shield size={16} />
          <span>Enterprise-Grade Security</span>
          <Shield size={16} />
        </div>
      </div>
    </div>
  );
}
