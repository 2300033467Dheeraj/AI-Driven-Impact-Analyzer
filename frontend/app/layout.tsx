import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Sidebar from '@/components/Sidebar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Impact Analyzer | AI-Driven Cloud Impact',
  description: 'AI-Driven Impact Analyzer for Cloud-Native Systems',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="bg-gray-950">
      <body className={`${inter.className} min-h-screen antialiased`}>
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="ml-64 flex-1 p-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
