/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  // Proxy API requests to the backend during local development
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (!apiUrl) {
      // No API URL set — proxy to local backend
      return [
        {
          source: '/api/v1/:path*',
          destination: 'http://127.0.0.1:8000/api/v1/:path*',
        },
        {
          source: '/health',
          destination: 'http://127.0.0.1:8000/health',
        },
      ];
    }
    return [];
  },
}

module.exports = nextConfig
