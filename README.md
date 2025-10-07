# agent-utils

Various utility APIs for agents

## Usage

Run directly:

```sh
uv run fastapi [dev|run]
```

Run the API in development or poduction mode.

Run production mode in a container:

```sh
docker run -p 8000:8000 --env-file .env agent-utils
```

## Functions

Find the API documentation at http://…:8000/docs.

### Transcribe audio

Post the URL of an audio file and get a text transcript returned. Currently works with MP3.

## Configuration

The app needs an OpenAI API key to work, in the `.env` file.

```toml
OPENAI_API_KEY=… # Open AI, API key for access to the Whisper API
```
