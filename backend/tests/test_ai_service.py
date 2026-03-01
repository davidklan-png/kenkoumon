"""
AI service abstraction layer tests (TDD).
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.ai_service import (
    AIServiceConfig,
    CloudTranscriptionService,
    CloudClaudeReportService,
    CloudGPTReportService,
    UserHostedReportService,
    get_transcription_service,
    get_report_service,
)


class TestAIServiceConfig:
    """Tests for AI service configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = AIServiceConfig()
        assert config.transcription_source == "cloud"
        assert config.llm_source == "cloud"

    def test_custom_config(self):
        """Test custom configuration."""
        config = AIServiceConfig(
            transcription_source="user-hosted",
            llm_source="user-hosted",
            ollama_url="http://custom:11434"
        )
        assert config.transcription_source == "user-hosted"
        assert config.llm_source == "user-hosted"
        assert config.ollama_url == "http://custom:11434"


class TestCloudTranscriptionService:
    """Tests for cloud transcription service."""

    @pytest.mark.asyncio
    async def test_transcribe_requires_api_key(self):
        """Test that API key is required."""
        with patch("core.config.settings.openai_api_key", None):
            with pytest.raises(ValueError, match="API key is required"):
                CloudTranscriptionService(api_key=None)

    @pytest.mark.asyncio
    async def test_transcribe_missing_file(self):
        """Test transcription with missing file."""
        service = CloudTranscriptionService(api_key="test-key")
        with pytest.raises(FileNotFoundError):
            await service.transcribe("/nonexistent/file.m4a")

    @pytest.mark.asyncio
    async def test_transcribe_success(self):
        """Test successful transcription."""
        service = CloudTranscriptionService(api_key="test-key")

        # Mock httpx response
        mock_response = MagicMock()
        mock_response.json.return_value = {"text": "テスト文字起こし"}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )

            # Mock file existence
            with patch("os.path.exists", return_value=True):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__ = MagicMock()
                    mock_open.return_value.__exit__ = MagicMock()
                    mock_open.return_value.read = MagicMock(return_value=b"fake audio")

                    result = await service.transcribe("fake.m4a", "ja")
                    assert result == "テスト文字起こし"


class TestCloudClaudeReportService:
    """Tests for Claude report generation service."""

    @pytest.mark.asyncio
    async def test_generate_requires_api_key(self):
        """Test that API key is required."""
        with patch("core.config.settings.anthropic_api_key", None):
            with pytest.raises(ValueError, match="Anthropic API key is required"):
                CloudClaudeReportService(api_key=None)

    @pytest.mark.asyncio
    async def test_generate_report_success(self):
        """Test successful report generation."""
        service = CloudClaudeReportService(api_key="test-key")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [{"text": "# レポート\n\nテスト内容"}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )

            result = await service.generate_report(
                "テスト文字起こし",
                "テストプロンプト"
            )
            assert "# レポート" in result


class TestCloudGPTReportService:
    """Tests for GPT report generation service."""

    @pytest.mark.asyncio
    async def test_generate_report_success(self):
        """Test successful report generation."""
        service = CloudGPTReportService(api_key="test-key")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "# レポート\n\nテスト内容"}}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )

            result = await service.generate_report(
                "テスト文字起こし",
                "テストプロンプト"
            )
            assert "# レポート" in result


class TestUserHostedReportService:
    """Tests for user-hosted (Ollama) report generation."""

    @pytest.mark.asyncio
    async def test_generate_report_success(self):
        """Test successful report generation with Ollama."""
        service = UserHostedReportService(
            base_url="http://localhost:11434",
            model="llama3.1"
        )

        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "# レポート\n\nテスト内容"}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                return_value=mock_response
            )

            result = await service.generate_report(
                "テスト文字起こし",
                "テストプロンプト"
            )
            assert "# レポート" in result


class TestServiceFactory:
    """Tests for service factory functions."""

    def test_get_transcription_service_cloud(self):
        """Test getting cloud transcription service."""
        config = AIServiceConfig(openai_api_key="test-key")
        service = get_transcription_service("cloud", config)
        assert isinstance(service, CloudTranscriptionService)

    def test_get_report_service_claude(self):
        """Test getting Claude report service."""
        config = AIServiceConfig(anthropic_api_key="test-key")
        service = get_report_service("cloud", config, cloud_provider="claude")
        assert isinstance(service, CloudClaudeReportService)

    def test_get_report_service_gpt(self):
        """Test getting GPT report service."""
        config = AIServiceConfig(openai_api_key="test-key")
        service = get_report_service("cloud", config, cloud_provider="gpt")
        assert isinstance(service, CloudGPTReportService)

    def test_get_report_service_user_hosted(self):
        """Test getting user-hosted report service."""
        config = AIServiceConfig()
        service = get_report_service("user-hosted", config)
        assert isinstance(service, UserHostedReportService)
