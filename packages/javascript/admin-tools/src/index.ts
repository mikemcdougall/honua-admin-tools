/**
 * @honua/admin-tools
 * JavaScript/TypeScript admin tooling for Honua geospatial platform
 */

export interface HonuaAdminClientOptions {
  baseUrl: string;
  apiKey: string;
  timeout?: number;
  retryAttempts?: number;
}

export interface ServiceConfiguration {
  name: string;
  dataSource: string;
  layers: LayerConfiguration[];
}

export interface LayerConfiguration {
  name: string;
  table: string;
  geometryColumn?: string;
  spatialReference?: number;
}

export interface BulkImportOptions {
  serviceId: string;
  layerId: number;
  format: 'geojson' | 'shapefile' | 'csv';
  batchSize?: number;
  onProgress?: (progress: ImportProgress) => void;
}

export interface ImportProgress {
  processedCount: number;
  totalCount: number;
  percentage: number;
  message: string;
}

/**
 * Main admin client for Honua geospatial platform
 */
export class HonuaAdminClient {
  private options: Required<HonuaAdminClientOptions>;

  constructor(options: HonuaAdminClientOptions) {
    this.options = {
      timeout: 30000,
      retryAttempts: 3,
      ...options,
    };
  }

  /**
   * Create a new geospatial service
   */
  async createService(config: ServiceConfiguration): Promise<{ id: string; url: string }> {
    // Implementation would go here
    return { id: 'service-id', url: 'https://api.honua.com/services/service-id' };
  }

  /**
   * Import features in bulk with progress tracking
   */
  async importFeatures(options: BulkImportOptions): Promise<{ success: boolean; count: number }> {
    // Implementation would go here
    return { success: true, count: 1000 };
  }

  /**
   * List all services
   */
  async listServices(): Promise<ServiceConfiguration[]> {
    // Implementation would go here
    return [];
  }
}

// Export everything
export * from './react';
export * from './vue';