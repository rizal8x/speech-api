# Speech API

A high-performance Speech-to-Text (STT) and Text-to-Speech (TTS) API designed for Mini PCs, utilizing `faster-whisper` and `neutts-air`.

## Features

- **STT**: Powered by `faster-whisper`.
- **TTS**: Powered by `neutts-air`.
- **Optimized**: Uses PyTorch CPU builds (`torchao`, `intmm`) for efficient inference on CPU-only devices.
- **Framework**: Built with FastAPI.

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (for dependency management)

## Installation

1. Clone the repository.
2. Install dependencies using `uv`:

```bash
uv sync
```

This project specifically targets CPU usage with PyTorch optimized for CPU.

## Running the API

Start the server using `uv run`:

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Usage

### Health Check

```http
GET /health
```

### Speech to Text (STT)

Transcribe an audio file.

**Endpoint:** `POST /v1/speech/stt`

**Curl Example:**

```bash
curl -X POST "http://localhost:8000/v1/speech/stt" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/audio.wav"
```

**Response:**

```json
{
  "text": "Transcribed text...",
  "language": "en",
  "probability": 0.99
}
```

### Text to Speech (TTS)

Convert text to audio.

**Endpoint:** `POST /v1/speech/tts`

**Curl Example:**

```bash
curl -X POST "http://localhost:8000/v1/speech/tts" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{ "text": "Hello world" }' \
  --output output.wav
```

**Response:**
- Returns an `audio/wav` file.
