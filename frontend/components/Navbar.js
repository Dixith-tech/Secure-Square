import { Shield } from 'lucide-react';
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-gray-900 border-b border-gray-800 p-4">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        <Link href="/dashboard" className="flex items-center gap-2 text-white hover:text-blue-400">
          <Shield size={28} />
          <span className="text-xl font-bold">AI Security Platform</span>
        </Link>
        
        <div className="flex gap-6 text-white">
          <Link href="/dashboard" className="hover:text-blue-400">Dashboard</Link>
          <Link href="/login" className="hover:text-blue-400">Logout</Link>
        </div>
      </div>
    </nav>
  );
}
