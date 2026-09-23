import Link from 'next/link';

const navItems = [
  { href: '/dashboard', label: 'Дашборд' },
  { href: '/requests', label: 'Заявки' },
  { href: '/requests/new', label: 'Новая заявка' },
  { href: '/knowledge', label: 'База знаний' },
  { href: '/analytics', label: 'Аналитика' },
  { href: '/settings', label: 'Настройки' },
];

export function Sidebar() {
  return (
    <aside className="w-64 flex-shrink-0 border-r border-slate-200 bg-white px-4 py-6">
      <div className="mb-8 px-2">
        <p className="text-xs font-semibold uppercase tracking-wide text-brand-gold">
          ЭнергоКонтур
        </p>
        <h1 className="mt-2 text-lg font-semibold text-brand-navy">MVP Console</h1>
      </div>

      <nav className="space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block rounded-md px-3 py-2 text-sm text-slate-700 transition-colors hover:bg-brand-slate hover:text-brand-navy"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
