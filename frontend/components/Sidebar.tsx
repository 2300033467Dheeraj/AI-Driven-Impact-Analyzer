'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Layers, Server } from 'lucide-react';

const navItems = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/deployments', label: 'Deployments', icon: Layers },
  { href: '/services', label: 'Services', icon: Server },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-slate-800 bg-slate-950/95 backdrop-blur">
      <div className="flex h-full flex-col">
        <div className="border-b border-slate-800 px-6 py-5">
          <Link href="/" className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600">
              <Layers className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-white">
              Impact Analyzer
            </span>
          </Link>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {navItems.map(({ href, label, icon: Icon }) => {
            const isActive =
              pathname === href || (href !== '/' && pathname.startsWith(href));
            return (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-indigo-600/20 text-indigo-400'
                    : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                }`}
              >
                <Icon className="h-5 w-5 shrink-0" />
                {label}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-slate-800 px-4 py-3">
          <p className="text-xs text-slate-500">AI-Driven Cloud Impact</p>
          <p className="text-xs text-slate-600">v1.0.0</p>
        </div>
      </div>
    </aside>
  );
}
