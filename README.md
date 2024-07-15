# DiscordWebAgent

This project is a Discord bot that integrates with Google Search using a Large Language Model (LLM). The bot can process search queries and provide answers in the same language as the question.

## Features

- Utilizes Google Custom Search API for web searches.
- Integrates with Anthropic's Claude model for language processing.
- Handles search queries and provides structured responses.
- Logs messages and responses for easy debugging.

## Prerequisites

- Python 3.8 or higher
- Discord account and a bot token
- Google Cloud account with Custom Search API enabled
- Anthropic Claude model access

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yasuhiroinoue/DiscordWebAgent.git
    cd DiscordWebAgent
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your credentials:
    ```env
    GOOGLE_CSE_ID=your_google_cse_id
    GOOGLE_API_KEY=your_google_api_key
    CLAUDE_MODEL=your_claude_model
    GOOGLE_PROJECT=your_google_project
    GOOGLE_LOCATION=your_google_location
    DISCORD_BOT_TOKEN=your_discord_bot_token
    ```

## Usage

1. Run the bot:
    ```bash
    python web_search.py
    ```

2. Invite the bot to your Discord server using the OAuth2 URL provided by Discord.

3. Send a message to the bot in your Discord server to perform a search.

## Code Structure

- `web_search.py`: The main script that initializes the bot and handles search queries.
- `requirements.txt`: Lists the Python dependencies needed for the project.

## Functions

### prepare_message_content(content)

Formats the message content with a timestamp.

### get_agent_response(text)

Processes the input text using the LLM and Google Search API, returning the response and log message.

### send_log_message(channel, log_message)

Sends log messages to the Discord channel.

## Event Handlers

- `on_ready`: Logs a message when the bot is ready.
- `on_message`: Handles incoming messages and processes search queries.

## Logging

The bot uses Python's logging module to log information, which can be configured by adjusting the logging level.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
