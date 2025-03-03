import requests
from typing import Dict, Any, Optional


class ChatBotCRUD:
    def __init__(self, base_url: str = "http://localhost:5000"):
        """Initialize CRUD operations with base URL."""
        self.base_url = base_url.rstrip("/")
        # Verify server connection on initialization
        self._verify_server_connection()

    def _verify_server_connection(self) -> None:
        """Verify that the server is running and accessible."""
        try:
            response = requests.get(f"{self.base_url}/")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print(f"Warning: Could not connect to server at {self.base_url}")
            print("Please ensure the Flask server is running (python main.py)")
            print(
                "Default port is 5000. If using a different port, specify it in ChatBotCRUD initialization"
            )

    def create_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Create a new prompt.

        Args:
            prompt (str): The prompt text to be created

        Returns:
            Dict containing the created prompt and its index
        """
        try:
            response = requests.post(f"{self.base_url}/prompt", json={"prompt": prompt})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create prompt: {str(e)}")

    def get_response(self, prompt_index: int) -> Dict[str, str]:
        """
        Get ChatGPT response for a stored prompt.

        Args:
            prompt_index (int): Index of the stored prompt

        Returns:
            Dict containing the prompt and its response
        """
        try:
            response = requests.get(f"{self.base_url}/prompt/{prompt_index}")
            if response.status_code == 404:
                raise Exception("Prompt not found")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "json"):
                error_msg = e.response.json().get("error", str(e))
            else:
                error_msg = str(e)
            raise Exception(f"Failed to get response: {error_msg}")

    def update_prompt(self, prompt_index: int, new_prompt: str) -> Dict[str, Any]:
        """
        Update an existing prompt.

        Args:
            prompt_index (int): Index of the prompt to update
            new_prompt (str): New prompt text

        Returns:
            Dict containing the updated prompt and its index
        """
        try:
            response = requests.put(
                f"{self.base_url}/prompt/{prompt_index}", json={"prompt": new_prompt}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update prompt: {str(e)}")

    def delete_prompt(self, prompt_index: int) -> Dict[str, str]:
        """
        Delete a prompt.

        Args:
            prompt_index (int): Index of the prompt to delete

        Returns:
            Dict containing confirmation message and deleted prompt
        """
        try:
            response = requests.delete(f"{self.base_url}/prompt/{prompt_index}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to delete prompt: {str(e)}")
