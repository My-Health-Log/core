# Development Setup

## Prerequisites

- **nvm** - Install via [nvm-sh/nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
  ```bash
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  ```
- **Node.js 24.12.0+** - Installed via nvm (see below)
- **pnpm 10.13.1** - Install via `corepack enable && corepack prepare pnpm@10.13.1 --activate`

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
# Edit server/.env with your values

# Start development (server + client)
pnpm dev
```

## Available Commands

Run from `src/` (workspace root):

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start server and client in parallel |
| `pnpm dev:server` | Start server only |
| `pnpm dev:client` | Start client only |
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
    └── client/             # @mhl/client - React app
        ├── src/
        ├── package.json
        ├── tsconfig.json
        └── eslint.config.js
```

## Endpoints

### Server (localhost:3000)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ping` | Health check - returns `{"pong":"it worked!"}` |

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
