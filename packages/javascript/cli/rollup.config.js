import typescript from '@rollup/plugin-typescript';
import { dts } from 'rollup-plugin-dts';

const config = [
  // Main bundle
  {
    input: 'src/index.ts',
    output: {
      file: 'dist/index.js',
      format: 'cjs',
      exports: 'named',
    },
    external: ['commander', 'inquirer', 'ora', 'chalk', 'yaml'],
    plugins: [typescript({ tsconfig: './tsconfig.json' })],
  },
  // CLI executable
  {
    input: 'src/cli.ts',
    output: {
      file: 'dist/cli.js',
      format: 'cjs',
      banner: '#!/usr/bin/env node',
    },
    external: ['commander', 'inquirer', 'ora', 'chalk', 'yaml'],
    plugins: [typescript({ tsconfig: './tsconfig.json' })],
  },
  // Type definitions
  {
    input: 'src/index.ts',
    output: {
      file: 'dist/index.d.ts',
      format: 'es',
    },
    plugins: [dts()],
  },
];

export default config;