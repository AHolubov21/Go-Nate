# NATHAN Slack Bot

## Overview

NATHAN is a Slack bot designed to monitor Slack channels, analyze, and escalate alerts from other bots. It uses the Ollama for AI interaction and operates asynchronously to handle alerts with varying severity.

## Features

- Monitors multiple Slack channels.
- Identifies alerts based on predefined keywords.
- Escalates alerts based on priority and runbook instructions.
- Interacts with Slack via WebSocket.
- Uses llama.cpp and a local AI in AWS for AI interaction.
- Supports asynchronous operation.

## Requirements

- Python 3.8 or higher
- Docker
- Slack API token
- Ollama

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/nathan-slack-bot.git

2. Install dependencies:
pip install -r requirements.txt

3. Set up environment variables:
- `SLACK_TOKEN`: Your Slack API token.
- `OPENAI_API_KEY`: Your OpenAI API key.

## Configuration

Edit the `config.json` file to specify the Slack channels to monitor and other configurations.

## Usage

1. Run the bot:
python bot/main.py

2. The bot will start monitoring the specified Slack channels and handle alerts based on the configuration.
