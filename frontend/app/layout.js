import './globals.css';
import Navbar from '@/components/Navbar';

export const metadata = {
  title: 'AI Security Platform',
  description: 'Advanced threat detection and monitoring system',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-black text-white">
        <Navbar />
        {children}
      </body>
    </html>
  );
}
