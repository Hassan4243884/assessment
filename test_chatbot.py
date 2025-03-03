from crud_operations import ChatBotCRUD
import time


def test_chatbot_operations():
    """Test all CRUD operations of the ChatGPT Bot."""

    # Initialize the CRUD operations
    crud = ChatBotCRUD(base_url="http://localhost:5000")

    # Add a small delay to ensure server is ready
    time.sleep(1)

    try:
        # Test create_prompt
        print("\nTesting create_prompt...")
        result = crud.create_prompt("What is Python?")
        prompt_index = result["index"]
        print(f"Created prompt with index: {prompt_index}")

        # Add delay to allow server processing
        time.sleep(2)

        # Test get_response
        print("\nTesting get_response...")
        try:
            response = crud.get_response(prompt_index)
            print("Response:")
            print("-" * 80)
            print(response["response"])
            print("-" * 80 + "\n")
        except Exception as e:
            print(f"Error getting response: {str(e)}")

        # Add delay between operations
        time.sleep(1)

        # Test update_prompt
        print("\nTesting update_prompt...")
        try:
            update_result = crud.update_prompt(
                prompt_index, "What are the benefits of Python?"
            )
            print(f"Updated prompt: {update_result}")

            # Get response for updated prompt
            updated_response = crud.get_response(prompt_index)
            print("\nNew response:")
            print("-" * 80)
            print(updated_response["response"])
            print("-" * 80 + "\n")
        except Exception as e:
            print(f"Error updating prompt: {str(e)}")

        # Add delay between operations
        time.sleep(1)

        # Test delete_prompt
        print("\nTesting delete_prompt...")
        try:
            delete_result = crud.delete_prompt(prompt_index)
            print(f"Delete result: {delete_result}")
        except Exception as e:
            print(f"Error deleting prompt: {str(e)}")

    except Exception as e:
        print(f"Test failed: {str(e)}")


if __name__ == "__main__":
    test_chatbot_operations()
