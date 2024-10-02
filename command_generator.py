from openai import OpenAI
client = OpenAI()
# Set your OpenAI API key
#OPENAI_API_KEY='sk-U3Lva5hvrDffbg_Z-mR8wPhWb0CQF8xphEMf9TixSRT3BlbkFJHfAQSMjruc5fzhkRvxz1-3SxwM2JwH9AfZEuQBdx8A'

def generate_command(action):
    # Construct the prompt for the LLM
    prompt = f"Generate a sequence of commands to perform a robot action splitted only by a new line. The commands available are 'MFx', where 'MF' means moving forward and 'x' is the time in seconds for the following action, 'CCWa' where CCW represents counter clock wise rotations in a 'x' angle in degrees, and 'CWx' the clockwise rotation: {action}"

    try:
        # Call the OpenAI API to get a command
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the command from the response
        return completion.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {e}"