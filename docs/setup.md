# Development Setup

## Prerequisites

- **nvm** - Install via [nvm-sh/nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  ```
- **Node.js 24.12.0+** - Installed via nvm (see below)
- **pnpm 10.13.1** - Install via `corepack enable && corepack prepare pnpm@10.13.1 --activate`
- **Python 3.13+** - Required for PDF parsing service
- **uv** - Python package manager. Install via:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## Getting Started

```bash
# Clone and navigate to project
cd core/src

# Install and use correct Node version
nvm install   # Only needed first time, or if nvm use fails
nvm use

# Install all dependencies
pnpm install

# Setup environment variables
cp server/.env.example server/.env
# Edit server/.env with your values (see API Keys section below)

# Start development (server + client)
pnpm dev
```

## Available Commands

Run from `src/` (workspace root):

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start server, client, and PDF service in parallel |
| `pnpm dev:server` | Start server only |
| `pnpm dev:client` | Start client only |
| `pnpm dev:pdf-parse` | Start PDF parsing service (dev mode) |
| `pnpm start:pdf-parse` | Start PDF parsing service (production) |
| `pnpm build` | Build all packages |
| `pnpm test` | Run all tests |
| `pnpm lint` | Lint all packages |

## Package-Specific Commands

```bash
# Run command in specific package
pnpm --filter @mhl/server dev
pnpm --filter @mhl/client dev

# Add dependency to specific package
pnpm --filter @mhl/server add <package>

# Add shared dev dependency to root
pnpm add -D <package> -w
```

## Project Structure

```
core/
├── docs/                   # Documentation
└── src/                    # Workspace root
    ├── package.json        # Workspace scripts, shared devDeps
    ├── pnpm-workspace.yaml # Workspace config
    ├── eslint.config.js    # Shared ESLint config
    ├── .nvmrc              # Node version
    ├── server/             # @mhl/server - Fastify API
    │   ├── src/
    │   ├── package.json
    │   ├── tsconfig.json
    │   └── eslint.config.js
    ├── client/             # @mhl/client - React app
    │   ├── src/
    │   ├── package.json
    │   ├── tsconfig.json
    │   └── eslint.config.js
    └── pdf-parse/          # Python PDF extraction service
        ├── app/
        │   ├── main.py
        │   ├── routers/
        │   ├── services/
        │   └── schemas/
        ├── pyproject.toml  # uv project config
        └── uv.lock         # Python lockfile
```

## API Keys

### Google Gemini (required for AI features)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy the key and add to `server/.env`:
   ```
   GOOGLE_GENERATIVE_AI_API_KEY=your-api-key-here
   ```

## Endpoints

### Server (localhost:3000)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health/ping` | Health check - returns `{"pong":"it worked!"}` |
| GET | `/health/ai` | AI SDK health check - verifies Gemini integration |

### PDF Service (localhost:8000)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/extract` | Extract content from PDF (multipart/form-data) |

### Client (localhost:5173)

Vite dev server with HMR.

## Troubleshooting

### macOS esbuild approval popup

When first running `pnpm dev`, macOS may prompt to approve esbuild binary. This is safe - esbuild ships platform-specific native binaries that Gatekeeper verifies.

### "Cannot find module" errors

```bash
# Clean install
rm -rf node_modules server/node_modules client/node_modules
pnpm install
```

### Wrong Node version

```bash
nvm install  # Install version from .nvmrc (first time)
nvm use      # Switch to version from .nvmrc
```

### Python/uv issues

```bash
# Verify uv is installed
uv --version

# If pdf-parse deps fail, manually sync
cd src/pdf-parse
uv sync

# If Python version mismatch
uv python install 3.13

# Type checking (optional) - uses pyproject.toml config
npx pyright src/pdf-parse
```

### PDF service won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Run with explicit host/port
cd src/pdf-parse
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
