# News Agent (RSS + Gemini)

Autonomous news aggregation agent that fetches news from RSS feeds and summarizes them using Google Gemini AI.

## Features
- **Zero-cost Gathering**: Uses standard RSS feeds instead of paid News APIs.
- **Gemini Powered**: Intelligent summarization and strategic insights using Google's latest LLMs.
- **Simple & Lightweight**: No heavy frameworks, just pure Python.
- **Customizable**: Easily add your own RSS sources in `rss_engine.py`.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Set up your `.env` file:
   ```env
   GEMINI_API_KEY="your-google-ai-studio-key"
   GEMINI_MODEL="gemini-2.5-flash"
   ```

## Usage

Run the agent:
```bash
python3 src/main.py
```
Enter any topic (e.g., "React", "WebDev", "CSS") to get the latest news summary.

## Project Structure
- `src/main.py`: Entry point and CLI loop.
- `src/rss_engine.py`: Logic for fetching and filtering RSS feeds.
- `src/gemini_service.py`: Wrapper for Google Gemini SDK.
- `src/prompts.py`: Strategic summarization instructions.

## License
MIT
