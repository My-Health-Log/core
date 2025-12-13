# My Health Log

A privacy-first health data management app. Upload health reports, extract metrics via AI, and query your data through an LLM interface.

## Claude Code Guidelines

- **Do not write code unless explicitly asked.**
- Act as a reviewer and documentation helper.
- Suggest approaches, flag issues, and explain tradeoffs.
- When reviewing, be concise—point out problems, not style nitpicks.
- Help maintain this doc and other documentation as the project evolves.

## Project Structure

pnpm monorepo with scoped packages:

```
src/                        # Workspace root
├── package.json            # Workspace scripts, shared devDeps
├── pnpm-workspace.yaml     # Defines packages
├── .nvmrc                  # Node 24.12.0+
├── docker-compose.yml      # Postgres + server + client
├── server/                 # @mhl/server
│   └── package.json
└── client/                 # @mhl/client
    └── package.json
```

## Development

**Requirements:** Node 24.12.0+ (run `nvm use` from `src/`)

```bash
# From src/ (workspace root)
pnpm install              # Install all dependencies
pnpm dev                  # Run server + client in parallel
pnpm dev:server           # Server only
pnpm dev:client           # Client only
pnpm test                 # Run all tests
pnpm build                # Build all packages

# Or with Docker
docker compose up -d
```

## Tech Stack

**Server:**

- Fastify (Node.js) + `fastify-type-provider-zod`
- Drizzle ORM + Postgres
- AI SDK v5
- Zod for validation + type inference
- tsx for development

**Server structure:**

```
server/
├── src/
│   ├── app.ts              # Fastify instance + plugin registration
│   ├── server.ts           # Entry point (starts server)
│   ├── routes/
│   │   ├── index.ts        # Registers all routes
│   │   ├── health.ts       # /ping, /health
│   │   ├── auth.ts         # /auth/login, /auth/register
│   │   └── reports.ts      # /reports/upload, /reports/:id
│   ├── schemas/
│   │   ├── index.ts        # Re-exports all schemas
│   │   ├── auth.ts         # Login, register schemas
│   │   └── reports.ts      # Upload, metrics schemas
│   ├── services/
│   │   ├── ai.ts           # AI SDK wrapper
│   │   ├── ai.test.ts      # Unit test (colocated)
│   │   ├── encryption.ts   # Encrypt/decrypt health data
│   │   └── pdf.ts          # PDF parsing
│   ├── db/
│   │   ├── index.ts        # Drizzle client
│   │   ├── schema.ts       # Drizzle table definitions
│   │   └── migrations/     # SQL migrations
│   ├── plugins/
│   │   ├── swagger.ts      # Swagger config
│   │   └── auth.ts         # Auth hooks/decorators
│   ├── config/
│   │   └── index.ts        # Env vars, typed config
│   └── types/
│       └── index.ts        # Shared types (if needed)
└── tests/
    ├── integration/        # Route tests with test DB
    │   └── routes/
    │       └── auth.test.ts
    └── setup.ts            # Test DB setup, mocks
```

**Fastify patterns:**

- `app.ts` creates Fastify instance, `server.ts` starts it (separation aids testing)
- Routes are Fastify plugins with optional prefix: `app.register(auth, { prefix: '/auth' })`
- Middleware = hooks in `plugins/` (global) or inside routes (scoped)
- Hooks: `onRequest`, `preHandler`, `preSerialization` replace Express middleware

**Testing:**

- Unit tests colocated (`*.test.ts` next to source) - easy to spot coverage gaps
- Integration tests in `tests/integration/` - need test DB, different setup

**Client:**

- React 19 + Vite
- ESLint for linting
- TanStack Router (planned)

## Environment Variables

Server expects:

- `DATABASE_URL` - Postgres connection string

## Key Concepts

- No PII stored. Simple username/password + optional 2FA.
- Health data encrypted with user-held key.
- AI transcription extracts structured metrics from PDF reports.
- User can bring their own AI model key or use provided model.

## Testing

**Framework:** Vitest (both server and client for unified tooling)

```bash
# From src/ (workspace root)
pnpm test                        # All tests
pnpm --filter @mhl/server test   # Server only
pnpm --filter @mhl/client test   # Client only

# With coverage
pnpm --filter @mhl/server test:cov
```

**Coverage target:** 80%+ line coverage

**Test structure:**

```
server/tests/
├── unit/           # Pure functions, utilities, Zod schemas
├── integration/    # Routes with test DB (Fastify inject)
└── setup.ts        # Test DB setup, AI mocks

client/tests/
├── components/     # Vitest + React Testing Library
└── e2e/            # Playwright (critical user flows)
```

**Priority areas:**

- AI extraction logic (mock responses, verify parsing)
- Encryption/decryption (correctness is critical)
- Auth flows (password, 2FA)
- File upload handling (PDF validation, size limits)
- API routes (use Fastify's `inject()` for isolation)

## Current Focus

Setting up the server with Fastify + Drizzle.
