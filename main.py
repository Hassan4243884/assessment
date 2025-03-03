from flask import Flask, request, jsonify
from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv

app = Flask(__name__)


class ChatGPTBot:
    def __init__(self):
        self.prompts: List[str] = []  # Store prompts in memory
        self.initialize_gpt3()

    def initialize_gpt3(self) -> None:
        """Initialize OpenAI API with credentials from environment variables."""
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def create_prompt(self, prompt: str) -> Dict:
        """Store a new prompt and return its index."""
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt")

        self.prompts.append(prompt)
        return {"index": len(self.prompts) - 1, "prompt": prompt}

    def get_response(self, prompt_index: int) -> Dict:
        """Get ChatGPT response for a stored prompt."""
        if not 0 <= prompt_index < len(self.prompts):
            raise IndexError("Invalid prompt index")

        try:
            # Create a single, non-streaming completion
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": self.prompts[prompt_index]}],
                stream=False,  # Explicitly disable streaming
                max_tokens=500,  # Limit response length
            )

            # Extract the complete response
            response_text = response.choices[0].message.content.strip()

            return {"prompt": self.prompts[prompt_index], "response": response_text}
        except Exception as e:
            raise Exception(f"Error getting response from OpenAI: {str(e)}")

    def update_prompt(self, prompt_index: int, new_prompt: str) -> Dict:
        """Update an existing prompt at the given index."""
        if not 0 <= prompt_index < len(self.prompts):
            raise IndexError("Invalid prompt index")
        if not new_prompt or not isinstance(new_prompt, str):
            raise ValueError("Invalid prompt")

        self.prompts[prompt_index] = new_prompt
        return {"index": prompt_index, "prompt": new_prompt}

    def delete_prompt(self, prompt_index: int) -> Dict:
        """Delete a prompt at the given index."""
        if not 0 <= prompt_index < len(self.prompts):
            raise IndexError("Invalid prompt index")

        deleted_prompt = self.prompts.pop(prompt_index)
        return {
            "message": "Prompt deleted successfully",
            "deleted_prompt": deleted_prompt,
        }


# Initialize the ChatGPT bot
bot = ChatGPTBot()


@app.route("/prompt", methods=["POST"])
def create_prompt():
    """API endpoint to create a new prompt."""
    data = request.get_json()
    try:
        result = bot.create_prompt(data.get("prompt"))
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/prompt/<int:prompt_index>", methods=["GET"])
def get_response(prompt_index):
    """API endpoint to get response for a stored prompt."""
    try:
        if prompt_index < 0 or prompt_index >= len(bot.prompts):
            return jsonify({"error": "Invalid prompt index"}), 404

        result = bot.get_response(prompt_index)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/prompt/<int:prompt_index>", methods=["PUT"])
def update_prompt(prompt_index):
    """API endpoint to update an existing prompt."""
    data = request.get_json()
    try:
        result = bot.update_prompt(prompt_index, data.get("prompt"))
        return jsonify(result), 200
    except (IndexError, ValueError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/prompt/<int:prompt_index>", methods=["DELETE"])
def delete_prompt(prompt_index):
    """API endpoint to delete a prompt."""
    try:
        result = bot.delete_prompt(prompt_index)
        return jsonify(result), 200
    except IndexError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/")
def health_check():
    """Health check endpoint to verify server is running."""
    return jsonify({"status": "ok", "message": "Server is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
