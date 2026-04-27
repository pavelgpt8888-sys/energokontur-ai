# ЭнергоКонтур — MVP Skeleton

Технический скелет MVP для rule-based квалификации технических заявок на кабельные крепления.

## Технологии

- Next.js (App Router)
- TypeScript
- Tailwind CSS

## Что реализовано

- Базовый layout с левой навигацией
- Страницы с placeholder UI:
  - `/dashboard`
  - `/requests`
  - `/requests/new`
  - `/requests/[id]`
  - `/knowledge`
  - `/analytics`
  - `/settings`
- Минимальная структура без внешних AI API, n8n, Supabase, авторизации и CRM-интеграций

## Установка зависимостей

```bash
npm install
```

## Запуск локально

```bash
npm run dev
```

После запуска приложение доступно по адресу: `http://localhost:3000`.

## Основные команды

```bash
npm run dev     # запуск в режиме разработки
npm run build   # production-сборка
npm run start   # запуск production-сборки
npm run lint    # проверка линтером
```

## Примечания

- Корневая страница `/` автоматически перенаправляет на `/dashboard`.
- В текущей версии отсутствует сложная бизнес-логика — это намеренно, для базового MVP-скелета.
