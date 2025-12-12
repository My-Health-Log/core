# My Health Log

A privacy-first health data management app. Upload health reports, extract metrics via AI, and query your data through an LLM interface.

## Features

- Upload health reports (PDFs)
- AI-powered metric extraction
- Query your health data with natural language
- No PII stored - your data stays yours
- Bring your own AI model key (optional)

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| Server | Fastify, Drizzle ORM, Postgres, AI SDK v5, Zod |
| Client | React 19, Vite |
| Tooling | pnpm workspaces, TypeScript, ESLint, Vitest |

## Quick Start

```bash
cd src
nvm install && nvm use
pnpm install
pnpm dev
```

See [docs/setup.md](docs/setup.md) for detailed setup instructions.

## Documentation

- [Development Setup](docs/setup.md)
- [Tmux Setup](docs/tmux-setup.md) (optional)

## License

ISC
