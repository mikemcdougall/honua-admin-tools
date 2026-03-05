#!/usr/bin/env node

// Copyright (c) Honua Project Contributors. All rights reserved.
// Licensed under the Apache License, Version 2.0. See LICENSE in the project root.

import { Command } from 'commander';
import chalk from 'chalk';
import { ConfigCommand } from './commands/config';
import { ServicesCommand } from './commands/services';
import { ConnectionsCommand } from './commands/connections';
import { LayersCommand } from './commands/layers';
import { MetadataCommand } from './commands/metadata';
import { BulkCommand } from './commands/bulk';
import { VersionCommand } from './commands/version';

const program = new Command();

program
  .name('honua')
  .description('Honua Admin CLI - Administrative tools for Honua geospatial services')
  .version('1.0.0-alpha.1')
  .option('-v, --verbose', 'enable verbose logging')
  .option('--server-url <url>', 'server URL (can also be set via HONUA_SERVER_URL env var)')
  .option('--api-key <key>', 'API key (can also be set via HONUA_API_KEY env var)')
  .hook('preAction', (thisCommand, actionCommand) => {
    // Global setup
    if (thisCommand.opts().verbose) {
      process.env.HONUA_CLI_VERBOSE = 'true';
    }
  });

// Register commands
ConfigCommand(program);
ServicesCommand(program);
ConnectionsCommand(program);
LayersCommand(program);
MetadataCommand(program);
BulkCommand(program);
VersionCommand(program);

// Handle unknown commands
program.on('command:*', () => {
  console.error(chalk.red(`\nUnknown command: ${program.args.join(' ')}`));
  console.log('See --help for available commands.');
  process.exit(1);
});

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}

program.parse();