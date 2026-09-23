import type { ReactNode } from 'react';

type PageShellProps = {
  title: string;
  description: string;
  children?: ReactNode;
};

export function PageShell({ title, description, children }: PageShellProps) {
  return (
    <section className="space-y-6">
      <header className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-2xl font-semibold text-brand-navy">{title}</h2>
        <p className="mt-2 text-sm text-slate-600">{description}</p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            Основной блок
          </h3>
          <p className="mt-3 text-sm text-slate-700">
            Placeholder-контент для быстрой проверки структуры страницы.
          </p>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            Дополнительный блок
          </h3>
          <p className="mt-3 text-sm text-slate-700">
            Здесь позже будут данные и инструменты раздела.
          </p>
        </div>
      </div>

      {children}
    </section>
  );
}
