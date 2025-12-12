# Transcription

CLI tool to transcribe videos locally using OpenAI Whisper. The tool will also automatically translate non-English videos into English. Transcriptions can be embedded into the video as a subtitle track, onto the video stream itself, or just as a `.srt` file.

## Installation

### Prerequisites

The [uv Python package manager](https://docs.astral.sh/uv/getting-started/installation/) is required to build/run the project.

### Running in development

```bash
# Example usage:
uv run transcription --help
uv run transcription -v ./example-1.mp4 -v /path/to/example-2.mp4 -m medium -e soft
```

### Local installation

To make this tool globally available on your system, you can install it using uv.

```bash
uv tool install . -e
```

This makes the `transcription` command available for use anywhere on your system.

```bash
# Example usage:
transcription --help
```
