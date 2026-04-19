"""
Unit tests for SkyMechanics Platform database module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from db import FalkorDBClient, db_settings


class TestFalkorDBClient:
    """Tests for FalkorDBClient."""

    @patch('db.redis.Redis')
    def test_connect_success(self, mock_redis):
        """Test successful database connection."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        assert client._client is not None
        mock_redis.assert_called_once_with(
            host="localhost",
            port=6379,
            password=None,
            decode_responses=True
        )

    @patch('db.redis.Redis')
    def test_get_graph(self, mock_redis):
        """Test getting graph instance."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        
        with patch('db.Graph') as mock_graph:
            graph = client.get_graph()
            assert graph is not None
            mock_graph.assert_called_once()

    @patch('db.redis.Redis')
    def test_set_graph(self, mock_redis):
        """Test switching to a different graph."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="default")
        client.connect()
        
        with patch('db.Graph') as mock_graph:
            # Set initial graph
            initial_graph = client.get_graph()
            
            # Switch to tenant graph
            tenant_graph = client.set_graph("tenant_001")
            
            assert tenant_graph is not None
            assert mock_graph.call_count >= 2

    @patch('db.redis.Redis')
    def test_close_connection(self, mock_redis):
        """Test closing database connection."""
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        mock_client.ping.return_value = True
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        client.close()
        # Verify close was called on the client
        mock_client.close.assert_called_once()
        assert client._client is not None  # Client not set to None in implementation


class TestDatabaseSettings:
    """Tests for DatabaseSettings."""

    def test_default_settings(self):
        """Test default database settings."""
        assert db_settings.host == "localhost"
        assert db_settings.port == 6379
        assert db_settings.password is None
        assert db_settings.db_name == "skymechanics"


class TestDatabaseIntegration:
    """Integration tests for database operations."""

    def test_database_connection_parameters(self):
        """Test database connection uses correct parameters."""
        assert db_settings.host == "localhost"
        assert db_settings.port == 6379
