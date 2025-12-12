# Tmux Setup

This setup is completely optional. Tmux just makes it easier to setup and manage the project dev env.

## Prerequisites

- **tmux**
  - Install via [tmux repo](https://github.com/tmux/tmux/wiki/Installing)
  - Good setup to follow [here](https://www.youtube.com/watch?v=jaI3Hcw-ZaA)
- **tmuxifier** - Installed via tpm (installed in step above)

## Getting Started

```bash
# Navigate to the project and copy the contents of the example file
cd core && pbcopy < mhl-core.session.sh.example

# Create a new tmuxifier config and replace the contents with the copied file
# And replace the project placeholder <PATH-TO-REPO> with the correct one
tmuxifier ns mhl-core

# Start development (server + client)
tmuxifier s mhl-core
```

