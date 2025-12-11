# My Health Log

A privacy-first health data management app. Upload health reports, extract metrics via AI, and query your data through an LLM interface.

## Claude Code Guidelines

- **Do not write code unless explicitly asked.**
- Act as a reviewer and documentation helper.
- Suggest approaches, flag issues, and explain tradeoffs.
- When reviewing, be concise—point out problems, not style nitpicks.
- Help maintain this doc and other documentation as the project evolves.

## Project Structure
```
src/
├── docker-compose.yml    # Postgres + server + client
├── client/               # React + Vite
└── server/               # Fastify + Drizzle + AI SDK
```

## Development
```bash
# Start all services
docker compose up -d

# Or run individually
cd server && pnpm dev
cd client && pnpm dev
```

## Tech Stack

**Server:**
- Fastify (Node.js)
- Drizzle ORM + Postgres
- AI SDK v5
- Zod for validation

**Client:**
- React + Vite
- (TBD)

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
# Server
cd server && pnpm test           # Run tests
cd server && pnpm test:cov       # With coverage

# Client
cd client && pnpm test           # Component tests (Vitest + RTL)
cd client && pnpm test:e2e       # E2E tests (Playwright)
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
