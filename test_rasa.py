import requests
from services.GPTService import create_thread

# from config.config import RASA_URL

url = "https://rasa-test.onrender.com/webhooks/rest/webhook"


def run_rasa(user_uuid: str, message: str) -> str:
    payload = {
        "sender": user_uuid,
        "message": message,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError if one occurred

        # Check if the response is a JSON array and not empty
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get("text")
        else:
            return "No response text found in the Rasa response."

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., connection error, timeout)
        return f"RequestException: {str(e)}"

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 404, 500)
        return f"HTTPError: {str(e)}"

    except Exception as e:
        # Handle other exceptions
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    print("Running...")
    res = run_rasa(
        user_uuid="1111",
        message="My name is Lorenzo and you?",
    )
    print(res)

    # print(create_thread())

