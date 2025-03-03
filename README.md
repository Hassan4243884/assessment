# ChatGPT Bot API

A Flask-based ChatGPT Bot API with CRUD operations for managing prompts and getting responses from OpenAI's GPT-3.5 model.

## Features

- Create, Read, Update, and Delete prompts
- Interact with OpenAI's GPT-3.5 model
- RESTful API endpoints
- Error handling and input validation
- Separate CRUD operations interface

## Prerequisites

- Python 3.x
- OpenAI API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Hassan4243884/assessment
   cd chatgpt-bot-api
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask server:

   ```bash
   python main.py
   ```

2. The API will be available at `http://localhost:5000`

## API Endpoints

- `POST /prompt` - Create a new prompt
- `GET /prompt/<prompt_index>` - Get response for a stored prompt
- `PUT /prompt/<prompt_index>` - Update an existing prompt
- `DELETE /prompt/<prompt_index>` - Delete a prompt

## Testing

use `test_chatbot.py` to test the API.
