import typescript from '@rollup/plugin-typescript';
import { dts } from 'rollup-plugin-dts';

const config = [
  // Main bundle
  {
    input: 'src/index.ts',
    output: [
      {
        file: 'dist/index.js',
        format: 'cjs',
        exports: 'named',
      },
      {
        file: 'dist/index.mjs',
        format: 'es',
      },
    ],
    external: ['react', 'vue'],
    plugins: [typescript({ tsconfig: './tsconfig.json' })],
  },
  // React bundle
  {
    input: 'src/react.ts',
    output: [
      {
        file: 'dist/react.js',
        format: 'cjs',
        exports: 'named',
      },
      {
        file: 'dist/react.mjs',
        format: 'es',
      },
    ],
    external: ['react'],
    plugins: [typescript({ tsconfig: './tsconfig.json' })],
  },
  // Vue bundle
  {
    input: 'src/vue.ts',
    output: [
      {
        file: 'dist/vue.js',
        format: 'cjs',
        exports: 'named',
      },
      {
        file: 'dist/vue.mjs',
        format: 'es',
      },
    ],
    external: ['vue'],
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
  {
    input: 'src/react.ts',
    output: {
      file: 'dist/react.d.ts',
      format: 'es',
    },
    plugins: [dts()],
  },
  {
    input: 'src/vue.ts',
    output: {
      file: 'dist/vue.d.ts',
      format: 'es',
    },
    plugins: [dts()],
  },
];

export default config;