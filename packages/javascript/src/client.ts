// Copyright (c) Honua Project Contributors. All rights reserved.
// Licensed under the Apache License, Version 2.0. See LICENSE in the project root.

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { HonuaAdminApiError, HonuaAdminOperationError } from './errors';
import * as types from './types';

/**
 * Configuration options for the Honua Admin Client.
 */
export interface HonuaAdminClientOptions {
  /** The base URL of the Honua server */
  serverUrl: string;
  /** API key for authentication */
  apiKey: string;
  /** Request timeout in milliseconds (default: 30000) */
  timeout?: number;
  /** Additional headers to include with all requests */
  headers?: Record<string, string>;
}

/**
 * Client for the Honua Admin REST API.
 * Provides administrative functionality for managing Honua geospatial services.
 */
export class HonuaAdminClient {
  private readonly http: AxiosInstance;

  constructor(options: HonuaAdminClientOptions) {
    this.http = axios.create({
      baseURL: `${options.serverUrl.replace(/\/$/, '')}/admin/v1`,
      timeout: options.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': options.apiKey,
        ...options.headers,
      },
    });

    // Response interceptor for error handling
    this.http.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          const status = error.response.status;
          const data = error.response.data;
          throw new HonuaAdminApiError(
            data?.message || `HTTP ${status} error`,
            status,
            data
          );
        } else if (error.request) {
          throw new HonuaAdminOperationError(
            'Network error: No response received from server'
          );
        } else {
          throw new HonuaAdminOperationError(
            `Request configuration error: ${error.message}`
          );
        }
      }
    );
  }

  // Services

  /**
   * Lists all registered services.
   */
  async listServices(): Promise<types.ServiceSummary[]> {
    const response = await this.http.get<types.ServiceSummary[]>('/services');
    return response.data;
  }

  /**
   * Gets the settings for a specific service.
   */
  async getServiceSettings(serviceName: string): Promise<types.ServiceSettingsResponse> {
    const response = await this.http.get<types.ServiceSettingsResponse>(`/services/${serviceName}`);
    return response.data;
  }

  /**
   * Updates the enabled protocols for a service.
   */
  async updateProtocols(
    serviceName: string,
    protocols: string[]
  ): Promise<types.ServiceSettingsResponse> {
    const response = await this.http.patch<types.ServiceSettingsResponse>(
      `/services/${serviceName}/protocols`,
      { protocols }
    );
    return response.data;
  }

  // Connections

  /**
   * Lists all secure database connections.
   */
  async listConnections(): Promise<types.SecureConnectionSummary[]> {
    const response = await this.http.get<types.SecureConnectionSummary[]>('/connections');
    return response.data;
  }

  /**
   * Creates a new secure database connection.
   */
  async createConnection(
    request: types.CreateSecureConnectionRequest
  ): Promise<types.SecureConnectionSummary> {
    const response = await this.http.post<types.SecureConnectionSummary>(
      '/connections',
      request
    );
    return response.data;
  }

  /**
   * Tests a connection before saving.
   */
  async testDraftConnection(
    request: types.CreateSecureConnectionRequest
  ): Promise<types.ConnectionTestResult> {
    const response = await this.http.post<types.ConnectionTestResult>(
      '/connections/test',
      request
    );
    return response.data;
  }

  /**
   * Updates an existing secure database connection.
   */
  async updateConnection(
    id: string,
    request: types.UpdateSecureConnectionRequest
  ): Promise<types.SecureConnectionSummary> {
    const response = await this.http.patch<types.SecureConnectionSummary>(
      `/connections/${id}`,
      request
    );
    return response.data;
  }

  /**
   * Deletes a secure database connection.
   */
  async deleteConnection(id: string): Promise<void> {
    await this.http.delete(`/connections/${id}`);
  }

  // Layers

  /**
   * Lists published layers for a connection.
   */
  async listLayers(
    connectionId: string,
    serviceName?: string
  ): Promise<types.PublishedLayerSummary[]> {
    const params = serviceName ? { serviceName } : undefined;
    const response = await this.http.get<types.PublishedLayerSummary[]>(
      `/connections/${connectionId}/layers`,
      { params }
    );
    return response.data;
  }

  /**
   * Publishes a PostGIS table as a layer.
   */
  async publishLayer(
    connectionId: string,
    request: types.PublishLayerRequest
  ): Promise<types.PublishedLayerSummary> {
    const response = await this.http.post<types.PublishedLayerSummary>(
      `/connections/${connectionId}/layers`,
      request
    );
    return response.data;
  }

  /**
   * Enables or disables a specific layer.
   */
  async setLayerEnabled(
    connectionId: string,
    layerId: number,
    enabled: boolean,
    serviceName?: string
  ): Promise<types.PublishedLayerSummary> {
    const params = serviceName ? { serviceName } : undefined;
    const response = await this.http.patch<types.PublishedLayerSummary>(
      `/connections/${connectionId}/layers/${layerId}`,
      { enabled },
      { params }
    );
    return response.data;
  }

  // Discovery

  /**
   * Discovers PostGIS tables available on a connection.
   */
  async discoverTables(connectionId: string): Promise<types.TableDiscoveryResponse> {
    const response = await this.http.get<types.TableDiscoveryResponse>(
      `/connections/${connectionId}/discover`
    );
    return response.data;
  }

  // Metadata Resources

  /**
   * Lists metadata resources, optionally filtered by kind and namespace.
   */
  async listMetadataResources(
    kind?: string,
    ns?: string
  ): Promise<types.MetadataResource[]> {
    const params: Record<string, string> = {};
    if (kind) params.kind = kind;
    if (ns) params.ns = ns;

    const response = await this.http.get<types.MetadataResource[]>(
      '/metadata',
      { params }
    );
    return response.data;
  }

  /**
   * Gets a specific metadata resource by its identifier.
   */
  async getMetadataResource(
    kind: string,
    ns: string,
    name: string
  ): Promise<{ resource: types.MetadataResource; etag?: string }> {
    const response = await this.http.get<types.MetadataResource>(
      `/metadata/${kind}/${ns}/${name}`
    );
    return {
      resource: response.data,
      etag: response.headers.etag,
    };
  }

  /**
   * Creates a new metadata resource.
   */
  async createMetadataResource(
    resource: types.MetadataResource
  ): Promise<types.MetadataResource> {
    const response = await this.http.post<types.MetadataResource>('/metadata', resource);
    return response.data;
  }

  /**
   * Updates an existing metadata resource.
   */
  async updateMetadataResource(
    kind: string,
    ns: string,
    name: string,
    resource: types.MetadataResource,
    ifMatch?: string
  ): Promise<types.MetadataResource> {
    const headers = ifMatch ? { 'If-Match': ifMatch } : undefined;
    const response = await this.http.put<types.MetadataResource>(
      `/metadata/${kind}/${ns}/${name}`,
      resource,
      { headers }
    );
    return response.data;
  }

  /**
   * Deletes a metadata resource.
   */
  async deleteMetadataResource(
    kind: string,
    ns: string,
    name: string,
    ifMatch?: string
  ): Promise<void> {
    const headers = ifMatch ? { 'If-Match': ifMatch } : undefined;
    await this.http.delete(`/metadata/${kind}/${ns}/${name}`, { headers });
  }

  // Manifests

  /**
   * Gets the admin API capabilities.
   */
  async getCapabilities(): Promise<types.AdminCapabilitiesResponse> {
    const response = await this.http.get<types.AdminCapabilitiesResponse>('/capabilities');
    return response.data;
  }

  /**
   * Exports the metadata manifest.
   */
  async getManifest(ns?: string): Promise<types.MetadataManifest> {
    const params = ns ? { ns } : undefined;
    const response = await this.http.get<types.MetadataManifest>('/manifest', { params });
    return response.data;
  }

  /**
   * Applies a metadata manifest.
   */
  async applyManifest(
    request: types.ManifestApplyRequest
  ): Promise<types.ManifestApplyResult> {
    const response = await this.http.post<types.ManifestApplyResult>('/manifest', request);
    return response.data;
  }

  // Bulk Operations

  /**
   * Performs a bulk import operation.
   */
  async bulkImport(
    connectionId: string,
    request: types.BulkImportRequest
  ): Promise<types.BulkOperationResult> {
    const formData = new FormData();
    formData.append('connectionId', connectionId);
    formData.append('serviceName', request.serviceName);

    if (request.file) {
      formData.append('file', request.file);
    }

    if (request.options) {
      formData.append('options', JSON.stringify(request.options));
    }

    const response = await this.http.post<types.BulkOperationResult>(
      '/bulk/import',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  /**
   * Performs a bulk export operation.
   */
  async bulkExport(request: types.BulkExportRequest): Promise<types.BulkOperationResult> {
    const response = await this.http.post<types.BulkOperationResult>('/bulk/export', request);
    return response.data;
  }
}