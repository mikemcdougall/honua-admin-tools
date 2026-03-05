"""
Tests for data models.
"""

import pytest
from pydantic import ValidationError

from honua_admin.models import (
    LayerConfiguration,
    ServiceConfiguration,
    BulkImportOptions,
    ImportProgress
)


def test_layer_configuration_valid():
    """Test valid layer configuration."""
    layer = LayerConfiguration(
        name='test-layer',
        table='test_table',
        geometry_column='geom',
        spatial_reference=4326
    )

    assert layer.name == 'test-layer'
    assert layer.table == 'test_table'
    assert layer.geometry_column == 'geom'
    assert layer.spatial_reference == 4326


def test_layer_configuration_defaults():
    """Test layer configuration with defaults."""
    layer = LayerConfiguration(
        name='test-layer',
        table='test_table'
    )

    assert layer.geometry_column == 'geom'  # Default
    assert layer.spatial_reference == 4326  # Default


def test_service_configuration_valid():
    """Test valid service configuration."""
    service = ServiceConfiguration(
        name='test-service',
        data_source='postgresql://localhost/test',
        layers=[
            LayerConfiguration(name='layer1', table='table1'),
            LayerConfiguration(name='layer2', table='table2')
        ]
    )

    assert service.name == 'test-service'
    assert service.data_source == 'postgresql://localhost/test'
    assert len(service.layers) == 2


def test_service_configuration_validation():
    """Test service configuration validation."""
    with pytest.raises(ValidationError):
        ServiceConfiguration(
            name='',  # Empty name should fail
            data_source='postgresql://localhost/test',
            layers=[]
        )


def test_bulk_import_options():
    """Test bulk import options."""
    options = BulkImportOptions(
        service_id='service-123',
        layer_id=0,
        format='geojson',
        batch_size=500
    )

    assert options.service_id == 'service-123'
    assert options.layer_id == 0
    assert options.format == 'geojson'
    assert options.batch_size == 500


def test_bulk_import_options_defaults():
    """Test bulk import options with defaults."""
    options = BulkImportOptions(
        service_id='service-123',
        layer_id=0
    )

    assert options.format == 'geojson'  # Default
    assert options.batch_size == 1000  # Default
    assert options.validation_mode == 'strict'  # Default
    assert options.overwrite is False  # Default


def test_import_progress():
    """Test import progress model."""
    progress = ImportProgress(
        processed_count=500,
        total_count=1000,
        percentage=50.0,
        message='Processing batch 5'
    )

    assert progress.processed_count == 500
    assert progress.total_count == 1000
    assert progress.percentage == 50.0
    assert progress.message == 'Processing batch 5'
    assert len(progress.errors) == 0  # Default empty list