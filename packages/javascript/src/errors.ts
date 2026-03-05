// Copyright (c) Honua Project Contributors. All rights reserved.
// Licensed under the Apache License, Version 2.0. See LICENSE in the project root.

/**
 * Base class for all Honua Admin errors.
 */
export class HonuaAdminError extends Error {
  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace?.(this, this.constructor);
  }
}

/**
 * Error thrown when an API request fails with an HTTP error response.
 */
export class HonuaAdminApiError extends HonuaAdminError {
  public readonly statusCode: number;
  public readonly response?: any;

  constructor(message: string, statusCode: number, response?: any) {
    super(message);
    this.statusCode = statusCode;
    this.response = response;
  }
}

/**
 * Error thrown when an operation fails due to client-side issues.
 */
export class HonuaAdminOperationError extends HonuaAdminError {
  constructor(message: string) {
    super(message);
  }
}