from openai import OpenAI
client = OpenAI()
# Set your OpenAI API key
#OPENAI_API_KEY=sk-U3Lva5hvrDffbg_Z-mR8wPhWb0CQF8xphEMf9TixSRT3BlbkFJHfAQSMjruc5fzhkRvxz1-3SxwM2JwH9AfZEuQBdx8A

def generate_command(action):
    # Construct the prompt for the LLM
    prompt = "Generate a sequence of commands to perform a robot action, each separated by a new line. " + \
         "The available commands are (if a new command is needed you can created it based on the previous ones): " + \
         "'ONx', where 'ON' means starting the engine at an analog speed 'x' (from 0 to 255); " + \
         "'OFF', to stop the robot; " + \
         "'MFx', where 'MF' means moving forward, and 'x' is the time in milliseconds for the action; " + \
         "'CCWx', where 'CCW' represents counterclockwise rotation by an angle 'x' in degrees; " + \
         f"'CWx', for clockwise rotation by an angle 'x' in degrees: {action}"

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