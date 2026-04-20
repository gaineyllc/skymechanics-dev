"""
Unit tests for SkyMechanics Platform database module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from db import FalkorDBClient, db_settings


class TestFalkorDBClient:
    """Tests for FalkorDBClient."""

    def test_default_settings(self):
        """Test default database settings."""
        settings = db_settings
        assert settings.host == "localhost"
        assert settings.port == 6379
        assert settings.password is None
        assert settings.db_name == "skymechanics"

    def test_database_connection_parameters(self):
        """Test database connection parameters from environment."""
        client = FalkorDBClient(host="test-host", port=6380, db_name="test-db")
        assert client.host == "test-host"
        assert client.port == 6380
        assert client.db_name == "test-db"

    @patch('falkordb.FalkorDB')
    def test_connect_success(self, mock_falkordb):
        """Test successful database connection."""
        mock_client = MagicMock()
        mock_falkordb.return_value = mock_client
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        
        assert client._client is not None
        mock_falkordb.assert_called_once_with(
            host="localhost",
            port=6379,
            password=None
        )

    @patch('falkordb.FalkorDB')
    def test_get_graph(self, mock_falkordb):
        """Test getting graph instance."""
        mock_client = MagicMock()
        mock_falkordb.return_value = mock_client
        mock_graph = MagicMock()
        mock_client.select_graph.return_value = mock_graph
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        
        graph = client.get_graph()
        assert graph is not None
        mock_client.select_graph.assert_called_once_with("test")

    @patch('falkordb.FalkorDB')
    def test_set_graph(self, mock_falkordb):
        """Test switching to a different graph."""
        mock_client = MagicMock()
        mock_falkordb.return_value = mock_client
        mock_graph = MagicMock()
        mock_client.select_graph.return_value = mock_graph
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        
        graph = client.set_graph("new_graph")
        assert graph is not None
        mock_client.select_graph.assert_called_with("new_graph")

    @patch('falkordb.FalkorDB')
    def test_close_connection(self, mock_falkordb):
        """Test closing database connection."""
        mock_client = MagicMock()
        mock_falkordb.return_value = mock_client
        
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        client.connect()
        
        client.close()
        
        mock_client.close.assert_called_once()
        assert client._graph is None


class TestDatabaseSettings:
    """Tests for DatabaseSettings."""

    def test_default_settings(self):
        """Test default database settings."""
        settings = db_settings
        assert settings.host == "localhost"
        assert settings.port == 6379
        assert settings.password is None
        assert settings.db_name == "skymechanics"


class TestDatabaseIntegration:
    """Integration tests for database module."""

    def test_database_connection_parameters(self):
        """Test database connection parameters."""
        client = FalkorDBClient(host="localhost", port=6379, db_name="test")
        
        assert client.host == "localhost"
        assert client.port == 6379
        assert client.db_name == "test"
