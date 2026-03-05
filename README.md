# Honua Admin Tools

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![NuGet Version](https://img.shields.io/nuget/v/Honua.Admin.Tools.svg)](https://www.nuget.org/packages/Honua.Admin.Tools)
[![NPM Version](https://img.shields.io/npm/v/@honua/admin-tools.svg)](https://www.npmjs.com/package/@honua/admin-tools)
[![PyPI Version](https://img.shields.io/pypi/v/honua-admin.svg)](https://pypi.org/project/honua-admin/)

**Multi-language admin tooling for Honua geospatial platform** - Supporting C#, JavaScript, Python, and CLI tools for service management, user administration, and bulk operations.

## 🚀 Features

- **Multi-Language Support**: C#, JavaScript, Python, and CLI tools
- **Service Management**: Create, configure, and deploy Honua geospatial services
- **User Administration**: Manage user accounts, roles, and permissions
- **Bulk Operations**: Import/export large datasets with progress tracking
- **Blazor Integration**: Pre-built UI components for admin interfaces
- **Cross-Platform CLI**: Command-line tool for CI/CD and automation
- **Open Source**: Apache 2.0 licensed for maximum flexibility

## 📦 Installation

### C# (.NET)
```bash
dotnet add package Honua.Admin.Tools
```

### JavaScript/TypeScript
```bash
npm install @honua/admin-tools
# or for CLI
npm install -g @honua/cli
```

### Python
```bash
pip install honua-admin
```

## 🏗️ Architecture Overview

This repository contains functionality-focused admin tooling, separated from the runtime SDK for clean separation of concerns:

- **Runtime Operations**: Use [honua-core-sdk](https://github.com/mikemcdougall/honua-core-sdk) for feature queries and spatial operations
- **Admin Operations**: Use this package for service management, bulk operations, and administration

## 📂 Package Structure

```
packages/
├── dotnet/              # C# Admin SDK
│   ├── Honua.Admin.Tools/       # Core admin library
│   └── Honua.Admin.Blazor/      # Blazor UI components
├── javascript/          # JavaScript/TypeScript tooling
│   ├── admin-tools/             # @honua/admin-tools package
│   └── cli/                     # @honua/cli package
└── python/              # Python admin tools
    └── honua-admin/             # honua-admin package
```

## 🔧 Usage Examples

### C# Admin SDK

```csharp
using Honua.Admin.Tools;

var adminClient = new HonuaAdminClient("https://api.honua.com", "your-api-key");

// Service Management
await adminClient.Services.CreateAsync(new CreateServiceRequest
{
    Name = "my-service",
    DataSource = "postgresql://localhost:5432/geodata",
    Layers = [new LayerConfig { Name = "parcels", Table = "parcels" }]
});

// Bulk Operations
await adminClient.BulkOperations.ImportFeaturesAsync(
    serviceId: "my-service",
    layerId: 0,
    filePath: "data.geojson",
    onProgress: progress => Console.WriteLine($"Imported {progress.ProcessedCount} features")
);
```

### JavaScript/TypeScript Admin Tools

```typescript
import { HonuaAdminClient } from '@honua/admin-tools';

const client = new HonuaAdminClient({
  baseUrl: 'https://api.honua.com',
  apiKey: 'your-api-key'
});

// Service Management
await client.services.create({
  name: 'my-service',
  dataSource: 'postgresql://localhost:5432/geodata',
  layers: [{ name: 'parcels', table: 'parcels' }]
});

// Bulk Import with Progress
await client.bulkOperations.importFeatures({
  serviceId: 'my-service',
  layerId: 0,
  file: fileData,
  onProgress: (progress) => console.log(`Imported ${progress.processedCount} features`)
});
```

### Python Admin Tools

```python
from honua_admin import HonuaAdminClient

client = HonuaAdminClient('https://api.honua.com', api_key='your-api-key')

# Service Management
await client.services.create({
    'name': 'my-service',
    'data_source': 'postgresql://localhost:5432/geodata',
    'layers': [{'name': 'parcels', 'table': 'parcels'}]
})

# Bulk Operations
async def progress_callback(progress):
    print(f"Imported {progress['processed_count']} features")

await client.bulk_operations.import_features(
    service_id='my-service',
    layer_id=0,
    file_path='data.geojson',
    on_progress=progress_callback
)
```

### CLI Tool

```bash
# Initialize configuration
honua config init --url https://api.honua.com --api-key your-key

# Service Management
honua service create my-service --data-source postgresql://localhost:5432/geodata

# Bulk Import
honua import features my-service 0 data.geojson --progress

# Deploy Service
honua service deploy --config ./service.yaml
```

## 🌐 Functionality-First Architecture

This tooling follows a **functionality-first architecture** pattern:

### Runtime vs Admin Separation

| Use Case | Package | Purpose |
|----------|---------|---------|
| **Feature Queries** | [honua-core-sdk](https://github.com/mikemcdougall/honua-core-sdk) | Runtime spatial operations |
| **Mobile Apps** | [honua-core-sdk](https://github.com/mikemcdougall/honua-core-sdk) | Field data collection |
| **Service Management** | honua-admin-tools | Deploy and configure services |
| **User Administration** | honua-admin-tools | Manage users and permissions |
| **Bulk Operations** | honua-admin-tools | Import/export large datasets |
| **CI/CD Automation** | honua-admin-tools | Automated deployment pipelines |

### Clear Boundaries

- **Runtime SDK**: Lightweight, focused on feature queries and spatial operations
- **Admin Tools**: Comprehensive tooling for management, administration, and bulk operations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[honua-core-sdk](https://github.com/mikemcdougall/honua-core-sdk)**: Runtime .NET library for production applications
- **[geospatial-grpc](https://github.com/mikemcdougall/geospatial-grpc)**: Protocol definitions for gRPC geospatial standards
- **[honua-server](https://github.com/mikemcdougall/honua-server)**: Server implementation

## 📞 Support

- [Issues](https://github.com/mikemcdougall/honua-admin-tools/issues): Bug reports and feature requests
- [Discussions](https://github.com/mikemcdougall/honua-admin-tools/discussions): Community support and questions

---

Built with ❤️ by the Honua Project Contributors