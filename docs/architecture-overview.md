# Honua SDK Architecture Overview

## Functionality-First Design

The Honua SDK ecosystem has been reorganized from a **platform-first** to a **functionality-first** approach, providing clear separation between runtime capabilities and administrative tooling.

## Current Architecture

### 1. Core Runtime SDKs (Platform-Focused)

These packages provide pure runtime capabilities for production applications:

#### **honua-core-sdk** (renamed from honua-core)
- **Package**: `Honua.Core.Sdk` (NuGet)
- **License**: Apache 2.0
- **Purpose**: Pure runtime .NET library for production applications
- **Features**:
  - Feature queries and spatial filtering
  - gRPC protocol conversion utilities
  - Cross-platform domain models
  - Transport abstractions
- **Repository**: `https://github.com/mikemcdougall/honua-core-sdk`

#### **honua-js-sdk** (future)
- **Package**: `@honua/sdk` (NPM)
- **License**: Apache 2.0
- **Purpose**: JavaScript runtime SDK for web and Node.js applications

#### **honua-python-sdk** (future)
- **Package**: `honua-sdk` (PyPI)
- **License**: Apache 2.0
- **Purpose**: Python runtime SDK for data science and server applications

#### **honua-mobile-sdk** (future)
- **Package**: `Honua.Mobile.Sdk` (NuGet)
- **License**: Apache 2.0
- **Purpose**: .NET MAUI mobile SDK for iOS/Android applications

### 2. Admin Tooling (Functionality-Focused)

#### **honua-admin-tools** (new repository)
- **Repository**: `https://github.com/mikemcdougall/honua-admin-tools`
- **License**: Apache 2.0
- **Purpose**: Multi-language administrative tooling

**Package Structure**:
```
honua-admin-tools/
├── packages/
│   ├── dotnet/                   # Honua.Admin.Tools NuGet
│   ├── javascript/               # @honua/admin-tools NPM
│   ├── python/                   # honua-admin PyPI
│   └── cli/                      # Cross-platform CLI
├── docs/
│   ├── automation-guide.md
│   ├── bulk-operations.md
│   └── api-reference.md
└── examples/
    ├── infrastructure-as-code/
    ├── migration-scripts/
    └── monitoring/
```

**Admin Packages**:
- **Honua.Admin.Tools** (.NET): Service management, bulk operations, automation
- **@honua/admin-tools** (JavaScript): Node.js admin automation and CI/CD
- **honua-admin** (Python): DevOps scripting, GeoPandas integration
- **@honua/cli** (CLI): Cross-platform command-line interface

## Key Administrative Features

### Service Management
- Service deployment and configuration
- Protocol management (REST, OGC, gRPC)
- Access policy configuration
- Health monitoring and diagnostics

### Data Operations
- Bulk import/export operations
- PostGIS table discovery and cataloging
- Layer publishing and management
- Style configuration and rendering

### Security & Connections
- Secure database connection management
- Encryption key rotation
- User and role administration
- Fine-grained access control

### Infrastructure
- Database schema migrations
- Performance monitoring and analytics
- Backup and recovery automation
- Environment-specific configurations

## Architecture Benefits

### 1. Clear Separation of Concerns
- **Runtime SDKs**: Focus exclusively on application functionality
- **Admin Tools**: Dedicated to operational and administrative tasks

### 2. Technology-Appropriate Solutions
- **.NET**: Strong for enterprise applications and mobile development
- **JavaScript/Node.js**: Excellent for DevOps automation and CI/CD
- **Python**: Perfect for data science workflows and GeoPandas integration
- **CLI**: Universal access across all platforms and environments

### 3. Licensing Clarity
- **Client SDKs & Admin Tools**: Apache 2.0 (fully open source)
- **gRPC Protocols**: Apache 2.0 (open standard)
- **Server Implementation**: ELv2 (source available)

### 4. Developer Experience
- **Targeted Packages**: Developers only install what they need
- **Consistent APIs**: Similar patterns across all language implementations
- **Rich Documentation**: Comprehensive guides and examples

## Migration Path

### From honua-core to honua-core-sdk
1. Update package reference: `Honua.Core` → `Honua.Core.Sdk`
2. No code changes required (same namespace and APIs)
3. Administrative functionality moved to `Honua.Admin.Tools`

### From Honua.Sdk.Admin to Honua.Admin.Tools
1. Update package reference: `Honua.Sdk.Admin` → `Honua.Admin.Tools`
2. Update namespace: `Honua.Sdk.Admin` → `Honua.Admin.Tools`
3. Same APIs and functionality, better organized

## Repository Structure

### Runtime Repositories
- `honua-core-sdk/`: Core .NET runtime SDK
- `honua-mobile-sdk/`: .NET MAUI mobile SDK (future)
- `honua-js-sdk/`: JavaScript runtime SDK (future)
- `honua-python-sdk/`: Python runtime SDK (future)

### Administrative Repository
- `honua-admin-tools/`: Multi-language admin tooling

### Infrastructure Repositories
- `geospatial-grpc/`: Open gRPC protocol definitions (Apache 2.0)
- `honua-server/`: Server implementation (ELv2)

## Usage Examples

### Runtime SDK Usage

```csharp
// .NET runtime application
using Honua.Core.Sdk;

var query = new FeatureQuery
{
    Where = "population > 100000",
    ReturnGeometry = true
};
```

### Admin Tools Usage

```csharp
// .NET administrative application
using Honua.Admin.Tools;

var adminClient = new HonuaAdminClient(options);
await adminClient.PublishLayerAsync(connectionId, publishRequest);
```

```python
# Python administrative script
from honua_admin import HonuaAdminClient

client = HonuaAdminClient(server_url='...', api_key='...')
services = client.list_services()
```

```bash
# CLI administrative commands
honua services list
honua layers publish --connection db-main --service analytics cities
```

## Future Roadmap

### Phase 1: Core SDK Stabilization
- Finalize honua-core-sdk v1.0
- Complete admin tools migration
- Comprehensive documentation

### Phase 2: Mobile SDK
- Release honua-mobile-sdk for .NET MAUI
- AR/VR capabilities for utility visualization
- Offline-first field data collection

### Phase 3: Multi-Language Expansion
- JavaScript runtime SDK
- Python runtime SDK with GeoPandas integration
- Enhanced CLI capabilities

### Phase 4: Open Standards Initiative
- Submit gRPC geospatial protocols to OGC
- Build industry ecosystem around open protocols
- Community-driven protocol evolution

This architecture provides a solid foundation for scaling the Honua ecosystem while maintaining clear boundaries between runtime and administrative functionality.