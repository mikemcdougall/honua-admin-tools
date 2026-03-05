// Copyright (c) Honua Project Contributors. All rights reserved.
// Licensed under the Apache License, Version 2.0. See LICENSE in the project root.

import { Command } from 'commander';
import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';
import os from 'os';
import inquirer from 'inquirer';

interface Config {
  serverUrl?: string;
  apiKey?: string;
  timeout?: number;
  outputFormat?: 'table' | 'json' | 'yaml';
}

const CONFIG_DIR = path.join(os.homedir(), '.honua');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

export class ConfigManager {
  static async load(): Promise<Config> {
    try {
      if (await fs.pathExists(CONFIG_FILE)) {
        return await fs.readJson(CONFIG_FILE);
      }
    } catch (error) {
      // Ignore errors, return empty config
    }
    return {};
  }

  static async save(config: Config): Promise<void> {
    await fs.ensureDir(CONFIG_DIR);
    await fs.writeJson(CONFIG_FILE, config, { spaces: 2 });
  }

  static async get(key: keyof Config): Promise<string | number | undefined> {
    const config = await this.load();
    return config[key];
  }

  static async set(key: keyof Config, value: string | number): Promise<void> {
    const config = await this.load();
    config[key] = value;
    await this.save(config);
  }

  static async remove(key: keyof Config): Promise<void> {
    const config = await this.load();
    delete config[key];
    await this.save(config);
  }

  static getEffectiveConfig(): Config {
    return {
      serverUrl: process.env.HONUA_SERVER_URL,
      apiKey: process.env.HONUA_API_KEY,
      timeout: process.env.HONUA_TIMEOUT ? parseInt(process.env.HONUA_TIMEOUT) : undefined,
    };
  }
}

export function ConfigCommand(program: Command) {
  const config = program
    .command('config')
    .description('Manage CLI configuration');

  config
    .command('set')
    .description('Set configuration values')
    .argument('<key>', 'configuration key (server-url, api-key, timeout, output-format)')
    .argument('<value>', 'configuration value')
    .action(async (key: string, value: string) => {
      try {
        const normalizedKey = key.replace(/-([a-z])/g, (g) => g[1].toUpperCase()) as keyof Config;

        if (!['serverUrl', 'apiKey', 'timeout', 'outputFormat'].includes(normalizedKey)) {
          console.error(chalk.red(`Unknown configuration key: ${key}`));
          console.log('Valid keys: server-url, api-key, timeout, output-format');
          process.exit(1);
        }

        let processedValue: string | number = value;
        if (normalizedKey === 'timeout') {
          const numValue = parseInt(value);
          if (isNaN(numValue) || numValue <= 0) {
            console.error(chalk.red(`Invalid timeout value: ${value}`));
            process.exit(1);
          }
          processedValue = numValue;
        } else if (normalizedKey === 'outputFormat') {
          if (!['table', 'json', 'yaml'].includes(value)) {
            console.error(chalk.red(`Invalid output format: ${value}`));
            console.log('Valid formats: table, json, yaml');
            process.exit(1);
          }
        }

        await ConfigManager.set(normalizedKey, processedValue);
        console.log(chalk.green(`✓ Set ${key} = ${value}`));
      } catch (error) {
        console.error(chalk.red(`Failed to set configuration: ${error}`));
        process.exit(1);
      }
    });

  config
    .command('get')
    .description('Get configuration value')
    .argument('[key]', 'configuration key (optional - shows all if omitted)')
    .action(async (key?: string) => {
      try {
        const storedConfig = await ConfigManager.load();
        const effectiveConfig = ConfigManager.getEffectiveConfig();

        // Merge stored and environment config
        const mergedConfig: Config = {
          ...storedConfig,
          ...Object.fromEntries(
            Object.entries(effectiveConfig).filter(([, value]) => value !== undefined)
          ),
        };

        if (key) {
          const normalizedKey = key.replace(/-([a-z])/g, (g) => g[1].toUpperCase()) as keyof Config;
          const value = mergedConfig[normalizedKey];
          if (value !== undefined) {
            console.log(value);
          } else {
            console.error(chalk.red(`Configuration key not found: ${key}`));
            process.exit(1);
          }
        } else {
          // Show all configuration
          console.log(chalk.bold('Current Configuration:'));
          console.log('');

          const keys: (keyof Config)[] = ['serverUrl', 'apiKey', 'timeout', 'outputFormat'];
          for (const configKey of keys) {
            const displayKey = configKey.replace(/([A-Z])/g, '-$1').toLowerCase();
            const value = mergedConfig[configKey];
            const source = effectiveConfig[configKey] !== undefined ? '(env)' : '(config)';

            if (value !== undefined) {
              const displayValue = configKey === 'apiKey' ? '***' : value;
              console.log(`  ${chalk.cyan(displayKey.padEnd(12))} ${displayValue} ${chalk.gray(source)}`);
            } else {
              console.log(`  ${chalk.gray(displayKey.padEnd(12) + '(not set)')}`);
            }
          }
        }
      } catch (error) {
        console.error(chalk.red(`Failed to get configuration: ${error}`));
        process.exit(1);
      }
    });

  config
    .command('unset')
    .description('Remove configuration value')
    .argument('<key>', 'configuration key to remove')
    .action(async (key: string) => {
      try {
        const normalizedKey = key.replace(/-([a-z])/g, (g) => g[1].toUpperCase()) as keyof Config;
        await ConfigManager.remove(normalizedKey);
        console.log(chalk.green(`✓ Removed ${key}`));
      } catch (error) {
        console.error(chalk.red(`Failed to remove configuration: ${error}`));
        process.exit(1);
      }
    });

  config
    .command('init')
    .description('Initialize configuration interactively')
    .action(async () => {
      try {
        console.log(chalk.bold('Honua CLI Configuration Setup'));
        console.log('');

        const answers = await inquirer.prompt([
          {
            type: 'input',
            name: 'serverUrl',
            message: 'Honua server URL:',
            validate: (input: string) => {
              if (!input.trim()) {
                return 'Server URL is required';
              }
              try {
                new URL(input);
                return true;
              } catch {
                return 'Please enter a valid URL';
              }
            },
          },
          {
            type: 'password',
            name: 'apiKey',
            message: 'API key:',
            validate: (input: string) => {
              if (!input.trim()) {
                return 'API key is required';
              }
              return true;
            },
          },
          {
            type: 'number',
            name: 'timeout',
            message: 'Request timeout (seconds):',
            default: 30,
            validate: (input: number) => {
              if (input <= 0) {
                return 'Timeout must be greater than 0';
              }
              return true;
            },
          },
          {
            type: 'list',
            name: 'outputFormat',
            message: 'Default output format:',
            choices: ['table', 'json', 'yaml'],
            default: 'table',
          },
        ]);

        const config: Config = {
          serverUrl: answers.serverUrl,
          apiKey: answers.apiKey,
          timeout: answers.timeout,
          outputFormat: answers.outputFormat,
        };

        await ConfigManager.save(config);

        console.log('');
        console.log(chalk.green('✓ Configuration saved successfully!'));
        console.log(chalk.gray(`Config file: ${CONFIG_FILE}`));
      } catch (error) {
        console.error(chalk.red(`Failed to initialize configuration: ${error}`));
        process.exit(1);
      }
    });
}