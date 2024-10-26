from openai import OpenAI
client = OpenAI()
# Set your OpenAI API key
#OPENAI_API_KEY=sk-U3Lva5hvrDffbg_Z-mR8wPhWb0CQF8xphEMf9TixSRT3BlbkFJHfAQSMjruc5fzhkRvxz1-3SxwM2JwH9AfZEuQBdx8A

def generate_command(action):
    # Construct the prompt for the LLM

#----- Examples -----
#     - Action: move forward with max speed for 3 seconds
#     - Response: ON255|MF3000|OFF

#     - Action: Start running
#     - Response: ON255

#     - Action: Stop running
#     - Response: OFF
    prompt = f"""
----- Instructions -----

Generate a sequence of commands to perform a robot action. Each command should be on a new line.
The available commands are:
   - 'ONx': Starts the engine at an analog speed 'x' (range: 100 to 255);
   - 'OFF': Stops the robot;
   - 'MFx': Moves the robot forward for 'x' milliseconds;
   - 'MBx': Moves the robot backwards for 'x' milliseconds;
   - 'BLx': Blinks an LED for 'x' milliseconds;
   - 'CCWx': Rotates the robot counterclockwise by an angle 'x' in degrees;
   - 'CWx': Rotates the robot clockwise by an angle 'x' in degrees.

Note: The sequence must start with 'ONx' and end with 'OFF', except when blinking the LED. Ensure that all values for 'x' (speed, time, and angle) are positive numbers.
Examples:

1
Action: move forward with max speed for 3 seconds
ON255
MF3000
OFF

2
Action: blink a LED for 3 seconds.
BL3000

3
Action: Start running
ON255

4
Action: Stop running
OFF

5
Action: Move backwards with 100% of speed for 5 seconds and when it stop blink a LED for 3 seconds.
ON255
MB5000
OFF
BL3000

6
Action: Rotate the robot counterclockwise by 90 degrees.
CCW90

7
Action: Rotate the robot clockwise by 180 degrees.
CW180

Our action is:
Action: {action}
"""

    try:
        # Call the OpenAI API to get a command
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the command from the response
        return completion.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {e}"
