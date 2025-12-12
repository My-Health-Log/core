import globals from 'globals'
import { defineConfig } from 'eslint/config'
import rootConfig from '../eslint.config.js';

export default defineConfig([
  ...rootConfig,
  {
    extends: [
    ],
    languageOptions: {
      globals: globals.node,
    },
  },
])
