"""
AI Service Abstraction Layer.

Supports multiple AI sources for transcription and report generation:
- On-device: whisper.cpp, llama.cpp (via HTTP endpoints from mobile)
- User-hosted: Ollama, LocalAI
- Cloud (optional): OpenAI, Anthropic
"""

import os
import httpx
from abc import ABC, abstractmethod
from typing import Optional, Literal
from core.config import settings


# =============================================================================
# AISource Configuration
# =============================================================================

AISource = Literal["on-device", "user-hosted", "cloud"]


class AIServiceConfig:
    """Configuration for AI services."""

    def __init__(
        self,
        transcription_source: AISource = settings.default_transcription_source,
        llm_source: AISource = settings.default_llm_source,
        ollama_url: str = settings.ollama_url,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
    ):
        self.transcription_source = transcription_source
        self.llm_source = llm_source
        self.ollama_url = ollama_url
        self.openai_api_key = openai_api_key or settings.openai_api_key
        self.anthropic_api_key = anthropic_api_key or settings.anthropic_api_key


# =============================================================================
# Transcription Services
# =============================================================================

class TranscriptionService(ABC):
    """Abstract base for transcription services."""

    @abstractmethod
    async def transcribe(self, audio_path: str, language: str = "ja") -> str:
        """Transcribe audio file to text."""
        pass


class OnDeviceTranscriptionService(TranscriptionService):
    """
    On-device transcription service.

    Note: For backend use, this expects audio to be processed on-device
    and the transcript sent via API. This is a placeholder for the interface.
    """

    async def transcribe(self, audio_path: str, language: str = "ja") -> str:
        """
        On-device transcription placeholder.

        In production, mobile apps handle on-device transcription
        and send the transcript to the backend.
        """
        raise NotImplementedError(
            "On-device transcription should be handled on the client device. "
            "Send the transcript directly via the API."
        )


class UserHostedTranscriptionService(TranscriptionService):
    """User-hosted transcription via Ollama or LocalAI."""

    def __init__(self, base_url: str = settings.ollama_url):
        self.base_url = base_url

    async def transcribe(self, audio_path: str, language: str = "ja") -> str:
        """
        Transcribe using user-hosted Whisper (via Ollama).

        Note: Ollama doesn't natively support Whisper. This is for
        LocalAI or similar OpenAI-compatible endpoints.
        """
        async with httpx.AsyncClient(timeout=300.0) as client:
            # For LocalAI with Whisper support
            url = f"{self.base_url}/v1/audio/transcriptions"

            # Check if file exists
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            with open(audio_path, "rb") as audio_file:
                files = {"file": audio_file}
                data = {"language": language}

                if "ollama" in self.base_url:
                    raise NotImplementedError(
                        "Ollama does not support Whisper. Use LocalAI or process on-device."
                    )

                response = await client.post(url, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                return result.get("text", "")


class CloudTranscriptionService(TranscriptionService):
    """Cloud transcription using OpenAI Whisper API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key is required for cloud transcription")

    async def transcribe(self, audio_path: str, language: str = "ja") -> str:
        """Transcribe using OpenAI Whisper API."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            url = "https://api.openai.com/v1/audio/transcriptions"

            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            headers = {"Authorization": f"Bearer {self.api_key}"}

            with open(audio_path, "rb") as audio_file:
                files = {
                    "file": (os.path.basename(audio_path), audio_file, "audio/m4a"),
                }
                data = {
                    "model": "whisper-1",
                    "language": language,
                }

                response = await client.post(url, headers=headers, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                return result.get("text", "")


# =============================================================================
# Report Generation Services
# =============================================================================

class ReportGenerationService(ABC):
    """Abstract base for report generation services."""

    @abstractmethod
    async def generate_report(self, transcript: str, prompt: str) -> str:
        """Generate a medical report from transcript."""
        pass


class OnDeviceReportService(ReportGenerationService):
    """
    On-device report generation service.

    Note: For backend use, this expects generation to happen on-device
    and the report sent via API.
    """

    async def generate_report(self, transcript: str, prompt: str) -> str:
        """
        On-device generation placeholder.

        In production, mobile apps handle on-device generation
        and send the report to the backend.
        """
        raise NotImplementedError(
            "On-device report generation should be handled on the client device. "
            "Send the report directly via the API."
        )


class UserHostedReportService(ReportGenerationService):
    """User-hosted report generation via Ollama."""

    def __init__(self, base_url: str = settings.ollama_url, model: str = "llama3.1"):
        self.base_url = base_url
        self.model = model

    async def generate_report(self, transcript: str, prompt: str) -> str:
        """Generate report using Ollama."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            url = f"{self.base_url}/api/generate"

            full_prompt = f"{prompt}\n\n{transcript}"

            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
            }

            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")


class CloudClaudeReportService(ReportGenerationService):
    """Cloud report generation using Anthropic Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.anthropic_api_key
        if not self.api_key:
            raise ValueError("Anthropic API key is required for Claude")

        self.api_url = "https://api.anthropic.com/v1/messages"

    async def generate_report(self, transcript: str, prompt: str) -> str:
        """Generate report using Claude API."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }

            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n{transcript}"
                    }
                ]
            }

            response = await client.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]


class CloudGPTReportService(ReportGenerationService):
    """Cloud report generation using OpenAI GPT API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key is required for GPT")

    async def generate_report(self, transcript: str, prompt: str) -> str:
        """Generate report using GPT-4 API."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            url = "https://api.openai.com/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "content-type": "application/json",
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": transcript
                    }
                ],
                "max_tokens": 4096,
            }

            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]


# =============================================================================
# Factory Functions
# =============================================================================

def get_transcription_service(
    source: AISource,
    config: AIServiceConfig
) -> TranscriptionService:
    """Get appropriate transcription service based on source."""
    services = {
        "on-device": OnDeviceTranscriptionService(),
        "user-hosted": UserHostedTranscriptionService(config.ollama_url),
        "cloud": CloudTranscriptionService(config.openai_api_key),
    }
    return services[source]


def get_report_service(
    source: AISource,
    config: AIServiceConfig,
    cloud_provider: Literal["claude", "gpt"] = "claude"
) -> ReportGenerationService:
    """Get appropriate report generation service based on source."""
    if source == "cloud":
        if cloud_provider == "claude":
            return CloudClaudeReportService(config.anthropic_api_key)
        else:
            return CloudGPTReportService(config.openai_api_key)

    services = {
        "on-device": OnDeviceReportService(),
        "user-hosted": UserHostedReportService(config.ollama_url),
    }
    return services[source]
