# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Flask-based microservice that provides text-to-speech functionality using Azure Cognitive Services. The service exposes a single REST endpoint that converts text to MP3 audio files using Azure's TTS service.

## Common Development Commands

### Local Development
```bash
# Install dependencies using conda
conda env create -f environment.yml
conda activate azure_speech_env

# Run the service locally
python main.py
# Service runs on http://localhost:5000

# Test the endpoint
curl -X POST http://localhost:5000/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "filename": "test"}'
```

### Docker Development
```bash
# Build container image
docker build -t tts-microservices .

# Run container locally
docker run -p 5000:5000 \
  -e SPEECH_KEY="your-azure-key" \
  -e SPEECH_REGION="your-region" \
  tts-microservices
```

### Testing the Service
The service expects POST requests to `/text-to-speech` with JSON payload:
```json
{
  "text": "Text to convert to speech",
  "filename": "output_name"  // optional, defaults to "output"
}
```

## Architecture and Code Structure

### Core Components
- **main.py**: Flask application with single `/text-to-speech` endpoint
- **azure_tts_service.py**: Azure TTS integration and audio synthesis logic
- **config.py**: Configuration management supporting both environment variables and JSON config

### Configuration System
The service uses a flexible configuration approach:
1. Environment variables take precedence
2. Falls back to `config.json` file (if present)
3. Uses sensible defaults for optional settings

Required configuration:
- `SPEECH_KEY`: Azure Cognitive Services subscription key
- `SPEECH_REGION`: Azure region (e.g., "eastus")

Optional configuration:
- `VOICE`: Voice model (defaults to "en-US-AvaNeural")
- `OUTPUT_DIR`: Audio output directory (defaults to "audio/")

### Audio Processing
- Uses Azure Cognitive Services Speech SDK
- Outputs 48kHz 192kbps MP3 format
- Files are saved to configurable output directory
- Error handling for TTS failures with detailed error messages

### Container Architecture
- Based on `continuumio/miniconda3` for Python environment management
- Uses conda environment defined in `environment.yml`
- Exposes port 5000 for Flask application
- Includes all dependencies via conda and pip

## GitHub Actions CI/CD

The repository includes automated Docker image building:
- Triggers on push to `main` branch or manual dispatch
- Builds and pushes to GitHub Container Registry
- Image tagged as `ghcr.io/{owner}/tts-microservices:latest`
- Uses Docker Buildx for multi-platform support

## Important Notes

### Security Considerations
- Never commit Azure API keys or credentials to the repository
- Use environment variables or secure secret management for production
- The service creates an `audio/` directory for output files

### Dependencies
- Python 3.11 with Flask for web framework
- Azure Cognitive Services Speech SDK version 1.38.0
- Conda for environment management
- Requires Azure Cognitive Services subscription for TTS functionality

### Error Handling
- Returns appropriate HTTP status codes (400 for bad requests, 500 for server errors)
- Logs errors to console for debugging
- Provides structured JSON error responses