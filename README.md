# Honua Admin Tools

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Honua Admin Tools** provides comprehensive administrative tooling for Honua geospatial services across multiple platforms and programming languages. This repository focuses on functionality-first organization with multi-language support for DevOps, automation, and administrative workflows.

## 🚀 Features

- **Multi-Language Support**: Admin tools available for .NET, JavaScript/Node.js, Python, and CLI
- **Service Management**: Deploy, configure, and monitor Honua services
- **Bulk Operations**: Import/export large datasets and perform batch operations
- **User Administration**: Manage users, roles, and access policies
- **Infrastructure Automation**: Infrastructure-as-code patterns and deployment scripts
- **Database Migrations**: Schema management and data migration tools
- **Performance Analytics**: Monitoring, metrics, and performance analysis
- **Cross-Platform CLI**: Unified command-line interface for all platforms

## 📦 Packages

### .NET Package

```bash
dotnet add package Honua.Admin.Tools
```

**Features:**
- Service deployment and configuration
- Bulk data operations
- User and role management
- Database migration tools
- Performance monitoring APIs

### JavaScript/Node.js Package

```bash
npm install @honua/admin-tools
```

**Features:**
- Node.js automation scripts
- CI/CD integration
- Bulk operations via REST APIs
- Infrastructure monitoring
- DevOps workflow automation

### Python Package

```bash
pip install honua-admin
```

**Features:**
- Data science and analytics workflows
- Bulk import/export operations
- Infrastructure automation with Python
- Integration with Jupyter notebooks
- GeoPandas and spatial data processing

### CLI Tool

```bash
# Install via npm (cross-platform)
npm install -g @honua/cli

# Or download platform-specific binaries
curl -fsSL https://get.honua.dev | sh
```

**Features:**
- Cross-platform command-line interface
- Service deployment and management
- Bulk operations from the command line
- Infrastructure monitoring and diagnostics
- Scriptable automation workflows

## 🏗️ Architecture

```
honua-admin-tools/
├── packages/
│   ├── dotnet/                   # Honua.Admin.Tools NuGet package
│   │   ├── src/
│   │   │   └── Honua.Admin.Tools/
│   │   └── tests/
│   ├── javascript/               # @honua/admin-tools NPM package
│   │   ├── src/
│   │   ├── tests/
│   │   └── package.json
│   ├── python/                   # honua-admin PyPI package
│   │   ├── src/
│   │   │   └── honua_admin/
│   │   ├── tests/
│   │   └── setup.py
│   └── cli/                      # Cross-platform CLI tool
│       ├── src/
│       ├── tests/
│       └── build/
├── docs/
│   ├── automation-guide.md
│   ├── bulk-operations.md
│   ├── api-reference.md
│   └── deployment-patterns.md
└── examples/
    ├── infrastructure-as-code/   # Terraform, ARM, CloudFormation
    ├── migration-scripts/        # Data migration examples
    └── monitoring/              # Monitoring and alerting setups
```

## 🔧 Key Administrative Features

### Service Management
- **Service Deployment**: Deploy and configure Honua services
- **Protocol Configuration**: Enable/disable REST, OGC, gRPC protocols
- **Access Policy Management**: Configure authentication and authorization
- **Health Monitoring**: Service health checks and diagnostics

### Data Operations
- **Bulk Import/Export**: Large-scale data import and export operations
- **Table Discovery**: Discover and catalog PostGIS tables
- **Layer Publishing**: Publish PostGIS tables as feature layers
- **Style Management**: Configure layer rendering and symbology

### Security & Connections
- **Secure Connections**: Manage encrypted database connections
- **Key Rotation**: Encryption key management and rotation
- **User Management**: Create and manage user accounts and roles
- **Access Control**: Fine-grained permission management

### Infrastructure
- **Database Migrations**: Schema versioning and migrations
- **Performance Monitoring**: Query performance and resource usage
- **Backup & Recovery**: Data backup and disaster recovery
- **Configuration Management**: Environment-specific configurations

## 🚀 Quick Start

### .NET

```csharp
using Honua.Admin.Tools;
using Microsoft.Extensions.DependencyInjection;

var services = new ServiceCollection();
services.AddHonuaAdminTools(options =>
{
    options.ServerUrl = "https://api.honua.dev";
    options.ApiKey = "your-admin-api-key";
});

var adminClient = services.BuildServiceProvider()
    .GetRequiredService<IHonuaAdminClient>();

// List all services
var services = await adminClient.ListServicesAsync();

// Publish a layer
await adminClient.PublishLayerAsync("connection-id", new PublishLayerRequest
{
    ServiceName = "my-service",
    TableName = "cities",
    LayerName = "World Cities"
});
```

### JavaScript/Node.js

```javascript
const { HonuaAdminClient } = require('@honua/admin-tools');

const client = new HonuaAdminClient({
    serverUrl: 'https://api.honua.dev',
    apiKey: 'your-admin-api-key'
});

// List all services
const services = await client.listServices();

// Bulk import data
await client.bulkImport('connection-id', {
    source: 'shapefile',
    file: './data/cities.shp',
    serviceName: 'my-service'
});
```

### Python

```python
from honua_admin import HonuaAdminClient
import geopandas as gpd

client = HonuaAdminClient(
    server_url='https://api.honua.dev',
    api_key='your-admin-api-key'
)

# List all services
services = client.list_services()

# Work with GeoPandas
gdf = gpd.read_file('cities.geojson')
client.bulk_import_geodataframe('connection-id', gdf, 'my-service')
```

### CLI

```bash
# Configure the CLI
honua config set server-url https://api.honua.dev
honua config set api-key your-admin-api-key

# List services
honua services list

# Publish a layer
honua layers publish connection-id \
  --service my-service \
  --table cities \
  --name "World Cities"

# Bulk import
honua import --connection connection-id \
  --service my-service \
  --file ./data/cities.shp
```

## 🌐 Integration Patterns

### Infrastructure as Code

```hcl
# Terraform example
resource "honua_service" "my_service" {
  name = "spatial-analytics"

  protocols = ["rest", "grpc", "ogc"]

  access_policy {
    public_read = true
    admin_role  = "spatial-admin"
  }
}

resource "honua_layer" "population_data" {
  service_name    = honua_service.my_service.name
  connection_id   = "postgres-main"
  table_name      = "population_by_city"
  layer_name      = "Population Data"

  style {
    type = "choropleth"
    field = "population"
    color_ramp = "blues"
  }
}
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Deploy Geospatial Services
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: honua/deploy-action@v1
        with:
          server-url: ${{ secrets.HONUA_SERVER_URL }}
          api-key: ${{ secrets.HONUA_API_KEY }}
          manifest: ./deploy/services.yml
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[honua-core-sdk](https://github.com/mikemcdougall/honua-core-sdk)**: Core .NET SDK for runtime applications
- **[honua-server](https://github.com/mikemcdougall/honua-server)**: Server implementation (ELv2)
- **[geospatial-grpc](https://github.com/mikemcdougall/geospatial-grpc)**: Open gRPC protocol definitions (Apache 2.0)
- **[honua-mobile-sdk](https://github.com/mikemcdougall/honua-mobile-sdk)**: .NET MAUI mobile SDK (Apache 2.0)

## 📞 Support

- [Issues](https://github.com/mikemcdougall/honua-admin-tools/issues): Bug reports and feature requests
- [Discussions](https://github.com/mikemcdougall/honua-admin-tools/discussions): Community support and questions
- [Documentation](https://docs.honua.dev/admin-tools): Complete documentation

---

**Democratizing geospatial development, one admin tool at a time.**

Built with ❤️ by the Honua Project Contributors