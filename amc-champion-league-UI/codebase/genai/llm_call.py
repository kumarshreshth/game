from openai import OpenAI

# Initialize the OpenAI client with your API key
# It's recommended to set your API key as an environment variable (OPENAI_API_KEY)
# or pass it directly like: client = OpenAI(api_key="YOUR_API_KEY")
client = OpenAI(api_key="sk-proj")

def get_chat_completion(user_message):
    """
    Sends a message to the OpenAI Chat Completion API and returns the response.
    """
    print(f"LLM Called with message: {user_message}")
    return user_message
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or another suitable model like "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries of sports match reports."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,  # Controls randomness; lower for more deterministic output
            max_tokens=150,   # Maximum number of tokens to generate in the response
        )
        result = completion.choices[0].message.content.strip()
        print(f"Response from LLM: {result}")
        return result
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    user_input = "Tell me a fun fact about space."
    response = get_chat_completion(user_input)
    print(f"User: {user_input}")
    print(f"Assistant: {response}")

    user_input_2 = "What is the capital of France?"
    response_2 = get_chat_completion(user_input_2)
    print(f"\nUser: {user_input_2}")
    print(f"Assistant: {response_2}")