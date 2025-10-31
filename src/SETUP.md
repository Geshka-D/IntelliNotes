# Инструкция по локальному запуску LectureSynth

Этот проект был создан в Figma Make. Чтобы запустить его локально на вашем компьютере, следуйте этим шагам:

## Предварительные требования

Убедитесь, что у вас установлено:

- **Node.js** (версия 18 или выше) - [Скачать](https://nodejs.org/)
- **npm** или **yarn** (обычно устанавливается вместе с Node.js)

Проверьте установку:

```bash
node --version
npm --version
```

## Шаг 1: Создание нового проекта

Откройте терминал и выполните команды:

```bash
# Создайте новый Vite проект с React + TypeScript
npm create vite@latest lecturesynth -- --template react-ts

# Перейдите в папку проекта
cd lecturesynth
```

## Шаг 2: Установка зависимостей

Установите необходимые библиотеки:

```bash
# Основные зависимости
npm install

# UI библиотеки
npm install @radix-ui/react-slot @radix-ui/react-progress @radix-ui/react-tabs
npm install class-variance-authority clsx tailwind-merge
npm install lucide-react
npm install sonner

# Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Шаг 3: Настройка Tailwind CSS

### 3.1 Создайте файл `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
}
```

### 3.2 Обновите файл `src/index.css`:

Замените содержимое файла на:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 262.1 83.3% 57.8%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 262.1 83.3% 57.8%;
    --radius: 0.5rem;
  }

  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
  }
}
```

## Шаг 4: Копирование файлов проекта

Скопируйте все файлы из Figma Make в ваш локальный проект:

1. Скопируйте `App.tsx` в `src/App.tsx`
2. Скопируйте всю папку `components` в `src/components`
3. Скопируйте содержимое `styles/globals.css` в `src/index.css` (если нужны дополнительные стили)

## Шаг 5: Обновите главный файл

Отредактируйте `src/main.tsx`:

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## Шаг 6: Запуск проекта

Теперь вы можете запустить проект:

```bash
npm run dev
```

Откройте браузер и перейдите по адресу: **http://localhost:5173**

## Возможные проблемы и решения

### Ошибка импорта компонентов

Если возникают ошибки импорта, убедитесь, что все пути в импортах начинаются с `./` или `../`:

```typescript
// Правильно
import { Button } from "./components/ui/button";

// Неправильно
import { Button } from "/components/ui/button";
```

### Ошибки TypeScript

Если TypeScript ругается на типы, добавьте в `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Структура проекта после настройки

```
lecturesynth/
├── node_modules/
├── public/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   ├── lecture-library.tsx
│   │   ├── lecture-view.tsx
│   │   ├── recording-panel.tsx
│   │   └── upload-panel.tsx
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## Дополнительные команды

```bash
# Запуск в режиме разработки
npm run dev

# Сборка для продакшена
npm run build

# Предварительный просмотр продакшен сборки
npm run preview
```

## Следующие шаги

После успешного запуска вы можете:

- Настроить интеграцию с реальным бэкендом для записи аудио
- Добавить API для транскрибации (например, OpenAI Whisper)
- Реализовать сохранение данных в базу данных
- Добавить аутентификацию пользователей

## Полезные ссылки

- [Документация Vite](https://vitejs.dev/)
- [Документация React](https://react.dev/)
- [Документация Tailwind CSS](https://tailwindcss.com/)
- [Shadcn UI](https://ui.shadcn.com/)

Если возникнут проблемы, проверьте консоль браузера (F12) для подробной информации об ошибках.