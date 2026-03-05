# @honua/admin-tools

[![NPM Version](https://img.shields.io/npm/v/@honua/admin-tools.svg)](https://www.npmjs.com/package/@honua/admin-tools)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**JavaScript/TypeScript admin tooling for Honua geospatial platform**

Part of the [honua-admin-tools](https://github.com/mikemcdougall/honua-admin-tools) ecosystem for multi-language admin operations.

## Installation

```bash
npm install @honua/admin-tools
# or
yarn add @honua/admin-tools
# or
pnpm add @honua/admin-tools
```

## Quick Start

```typescript
import { HonuaAdminClient } from '@honua/admin-tools';

const client = new HonuaAdminClient({
  baseUrl: 'https://api.honua.com',
  apiKey: 'your-api-key'
});

// Create a new service
const service = await client.createService({
  name: 'my-service',
  dataSource: 'postgresql://localhost:5432/geodata',
  layers: [{
    name: 'parcels',
    table: 'parcels',
    geometryColumn: 'geom'
  }]
});

// Import features with progress tracking
await client.importFeatures({
  serviceId: service.id,
  layerId: 0,
  format: 'geojson',
  onProgress: (progress) => {
    console.log(`Imported ${progress.processedCount} features`);
  }
});
```

## Framework Integration

### React

```tsx
import { HonuaAdminProvider, useHonuaAdmin } from '@honua/admin-tools/react';

function AdminApp() {
  return (
    <HonuaAdminProvider client={client}>
      <ServiceManager />
    </HonuaAdminProvider>
  );
}

function ServiceManager() {
  const { services, createService } = useHonuaAdmin();
  // Component implementation
}
```

### Vue

```vue
<script setup>
import { useHonuaAdmin } from '@honua/admin-tools/vue';

const { services, createService } = useHonuaAdmin();
</script>
```

## API Reference

### HonuaAdminClient

Main admin client for service management and bulk operations.

#### Methods

- `createService(config)` - Create a new geospatial service
- `listServices()` - List all services
- `importFeatures(options)` - Import features with progress tracking

## Architecture

This JavaScript package is part of the functionality-first architecture:

| Technology | Package | Purpose |
|------------|---------|---------|
| **JavaScript** | @honua/admin-tools | Web admin interfaces |
| **CLI** | @honua/cli | Command-line operations |
| **.NET** | Honua.Admin.Tools | Blazor components |
| **Python** | honua-admin | Scripting and automation |

## Documentation

See the [honua-admin-tools repository](https://github.com/mikemcdougall/honua-admin-tools) for complete documentation and examples.

## License

Licensed under the Apache License, Version 2.0.