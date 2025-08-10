# TTS Microservices

A Flask-based microservice that provides text-to-speech functionality using Azure Cognitive Services. Part of the 40docs platform ecosystem.

## Features

- REST API endpoint for text-to-speech conversion
- Azure Cognitive Services integration
- MP3 audio output with configurable quality
- Docker containerization
- Flexible configuration via environment variables or JSON
- Automated CI/CD pipeline with GitHub Actions

## Quick Start

### Prerequisites

- Azure Cognitive Services subscription with Speech service
- Python 3.11+ or Docker
- Conda (for local development)

### Local Development

1. **Clone and setup environment:**
   ```bash
   git clone <repository-url>
   cd tts-microservices
   
   # Create conda environment
   conda env create -f environment.yml
   conda activate azure_speech_env
   ```

2. **Configure Azure credentials:**
   ```bash
   export SPEECH_KEY="your-azure-speech-key"
   export SPEECH_REGION="your-azure-region"  # e.g., "eastus"
   ```

3. **Run the service:**
   ```bash
   python main.py
   ```
   Service will be available at `http://localhost:5000`

### Docker Deployment

```bash
# Build the image
docker build -t tts-microservices .

# Run the container
docker run -p 5000:5000 \
  -e SPEECH_KEY="your-azure-key" \
  -e SPEECH_REGION="your-region" \
  tts-microservices
```

## API Usage

### Text-to-Speech Endpoint

**POST** `/text-to-speech`

Convert text to speech and save as MP3 file.

#### Request Body

```json
{
  "text": "Hello, this is a test message",
  "filename": "output_name"  // optional, defaults to "output"
}
```

#### Response

**Success (200):**
```json
{
  "path": "/app/audio/output_name.mp3"
}
```

**Error (400/500):**
```json
{
  "error": "Error description"
}
```

#### Example Usage

```bash
curl -X POST http://localhost:5000/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to the 40docs platform",
    "filename": "welcome"
  }'
```

## Configuration

The service supports multiple configuration methods with the following priority:

1. Environment variables (highest priority)
2. `config.json` file
3. Default values (lowest priority)

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `SPEECH_KEY` | Azure Cognitive Services key | *Required* |
| `SPEECH_REGION` | Azure region | *Required* |
| `VOICE` | Voice model to use | `en-US-AvaNeural` |
| `OUTPUT_DIR` | Audio output directory | `audio` |

### Example config.json

```json
{
  "speech_key": "your-azure-key",
  "speech_region": "eastus",
  "voice": "en-US-JennyNeural",
  "output_dir": "audio"
}
```

## Architecture

### Components

- **main.py**: Flask application with REST API endpoint
- **azure_tts_service.py**: Azure TTS service integration
- **config.py**: Configuration management layer
- **Dockerfile**: Container image definition
- **environment.yml**: Conda environment specification

### Audio Output

- **Format**: MP3 (48kHz, 192kbps, Mono)
- **Location**: Configurable output directory (default: `audio/`)
- **Naming**: `{filename}.mp3`

## Development

### Dependencies

- **Python**: 3.11
- **Flask**: Web framework
- **Azure Cognitive Services Speech SDK**: 1.38.0
- **Conda**: Environment management

### Testing

Test the service with different voices and text samples:

```bash
# Test with different voice
export VOICE="en-US-AriaNeural"

# Test with longer text
curl -X POST http://localhost:5000/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a longer text sample to test the text-to-speech functionality with more comprehensive content.",
    "filename": "long_test"
  }'
```

## CI/CD

The repository includes automated Docker image building via GitHub Actions:

- **Triggers**: Push to main branch or manual dispatch
- **Registry**: GitHub Container Registry (GHCR)
- **Image**: `ghcr.io/{owner}/tts-microservices:latest`

## Security

- **Credentials**: Never commit Azure API keys to the repository
- **Environment**: Use environment variables or secure secret management
- **Container**: Runs on port 5000 with minimal privileges

## Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify `SPEECH_KEY` and `SPEECH_REGION` are correctly set
- Ensure Azure subscription is active and has Speech service quota

**Audio Generation Failures:**
- Check output directory permissions
- Verify disk space availability
- Review Azure service limits and quotas

**Container Issues:**
- Ensure environment variables are properly passed to container
- Check container logs: `docker logs <container-id>`
- Verify port mapping: `-p 5000:5000`

### Logs

The service logs errors to console. Check application logs for detailed error information:

```bash
# Local development
python main.py

# Docker container
docker logs <container-name>
```

## License

Part of the 40docs platform ecosystem. See individual repository licenses for details.