// Copyright (c) Honua Project Contributors. All rights reserved.
// Licensed under the Apache License, Version 2.0. See LICENSE in the project root.

// Service Types
export interface ServiceSummary {
  name: string;
  displayName: string;
  enabled: boolean;
  protocols: string[];
  lastModified: string;
}

export interface ServiceSettingsResponse {
  serviceName: string;
  settings: ServiceSettings;
}

export interface ServiceSettings {
  displayName: string;
  enabled: boolean;
  protocols: string[];
  mapServer?: MapServerSettings;
  accessPolicy?: AccessPolicy;
  timeInfo?: TimeInfo;
}

export interface MapServerSettings {
  enabled: boolean;
  maxImageWidth?: number;
  maxImageHeight?: number;
  maxRecordCount?: number;
}

export interface AccessPolicy {
  publicRead: boolean;
  adminRole?: string;
  readRoles?: string[];
  writeRoles?: string[];
}

export interface TimeInfo {
  enabled: boolean;
  timeField?: string;
  timeExtent?: [string, string];
}

// Connection Types
export interface SecureConnectionSummary {
  id: string;
  name: string;
  description?: string;
  connectionString: string;
  enabled: boolean;
  lastTested?: string;
  testStatus?: 'success' | 'failure' | 'pending';
}

export interface SecureConnectionDetail {
  id: string;
  name: string;
  description?: string;
  connectionString: string;
  enabled: boolean;
  lastTested?: string;
  testStatus?: 'success' | 'failure' | 'pending';
  metadata?: Record<string, any>;
}

export interface CreateSecureConnectionRequest {
  name: string;
  description?: string;
  connectionString: string;
  enabled?: boolean;
  metadata?: Record<string, any>;
}

export interface UpdateSecureConnectionRequest {
  name?: string;
  description?: string;
  connectionString?: string;
  enabled?: boolean;
  metadata?: Record<string, any>;
}

export interface ConnectionTestResult {
  success: boolean;
  message: string;
  details?: Record<string, any>;
}

// Layer Types
export interface PublishedLayerSummary {
  layerId: number;
  serviceName: string;
  layerName: string;
  tableName: string;
  enabled: boolean;
  geometryType: string;
  srid: number;
  lastModified: string;
}

export interface PublishLayerRequest {
  serviceName: string;
  layerName: string;
  tableName: string;
  enabled?: boolean;
  geometryField?: string;
  srid?: number;
  metadata?: Record<string, any>;
}

// Discovery Types
export interface TableDiscoveryResponse {
  connectionId: string;
  tables: DiscoveredTable[];
  timestamp: string;
}

export interface DiscoveredTable {
  schema: string;
  tableName: string;
  geometryColumns: GeometryColumn[];
  recordCount?: number;
  lastModified?: string;
}

export interface GeometryColumn {
  columnName: string;
  geometryType: string;
  srid: number;
  dimensions: number;
}

// Metadata Types
export interface MetadataResource {
  apiVersion: string;
  kind: string;
  metadata: {
    name: string;
    namespace: string;
    labels?: Record<string, string>;
    annotations?: Record<string, string>;
  };
  spec: Record<string, any>;
  status?: Record<string, any>;
}

export interface AdminCapabilitiesResponse {
  version: string;
  features: string[];
  limits: {
    maxConnections?: number;
    maxServices?: number;
    maxLayers?: number;
  };
}

export interface MetadataManifest {
  apiVersion: string;
  kind: string;
  resources: MetadataResource[];
}

export interface ManifestApplyRequest {
  manifest: MetadataManifest;
  dryRun?: boolean;
  force?: boolean;
}

export interface ManifestApplyResult {
  applied: number;
  skipped: number;
  failed: number;
  errors?: string[];
}

// Bulk Operations
export interface BulkImportRequest {
  serviceName: string;
  file?: File | Buffer;
  format?: 'shapefile' | 'geojson' | 'csv';
  options?: {
    srid?: number;
    encoding?: string;
    delimiter?: string;
    geometryField?: string;
    overwrite?: boolean;
  };
}

export interface BulkExportRequest {
  serviceName: string;
  layerIds: number[];
  format: 'shapefile' | 'geojson' | 'csv' | 'geopackage';
  options?: {
    srid?: number;
    encoding?: string;
    includeMetadata?: boolean;
  };
}

export interface BulkOperationResult {
  operationId: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  recordsProcessed?: number;
  totalRecords?: number;
  errors?: string[];
  downloadUrl?: string;
}