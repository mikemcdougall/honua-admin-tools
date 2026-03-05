#!/usr/bin/env node

/**
 * CLI entry point for @honua/cli
 */

import { program } from 'commander';
import { HonuaCLI } from './index';

const cli = new HonuaCLI();

program
  .name('honua')
  .description('CLI tool for Honua geospatial platform administration')
  .version('1.0.0');

program
  .command('config')
  .description('Configure CLI settings')
  .command('init')
  .option('--url <url>', 'Honua API base URL')
  .option('--api-key <key>', 'API key for authentication')
  .action(async (options) => {
    await cli.init(options);
  });

program
  .command('service')
  .description('Service management commands');

program
  .command('deploy')
  .description('Deploy a service from configuration file')
  .argument('<config>', 'Path to service configuration file')
  .option('--environment <env>', 'Target environment', 'production')
  .option('--dry-run', 'Preview changes without deploying')
  .action(async (configPath, options) => {
    await cli.deployService(configPath, options);
  });

program
  .command('import')
  .description('Import data commands');

program
  .command('features')
  .description('Import features from file')
  .argument('<service-id>', 'Service ID')
  .argument('<layer-id>', 'Layer ID')
  .argument('<file>', 'Path to data file (GeoJSON, Shapefile, CSV)')
  .option('--progress', 'Show progress bar')
  .action(async (serviceId, layerId, filePath, options) => {
    await cli.importFeatures(serviceId, parseInt(layerId), filePath);
  });

if (require.main === module) {
  program.parse();
}