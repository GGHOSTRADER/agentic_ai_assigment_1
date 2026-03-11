"""
agent.py

This module contains the run_agent function which implements the financial assistant agent.
It handles user interactions, API calls, and tool invocations.
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from functions import available_functions
from schemas import tools


debug_log = False  # This flag can be toggled to enable/disable debug logging for tool calls and responses.


def run_agent():
    """
    Run the financial assistant agent loop.
    Handles user input, API calls, and tool invocations.
    """
    # Setup & Security
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    # System Prompt (Persona)
    messages = [
        {
            "role": "system",
            "content": "You are a Financial Assistant can tell exchange rate of a currency pair and prices of stocks. Use tools when needed and can request to use tools more than once if needed.",
        }
    ]

    print("Financial Assistant Agent Started. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        # First API Call
        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        if tool_calls:
            # Add the assistant's "thought" (tool call request) to history
            messages.append(response_msg)

            # Will print log of tool calls if debug_log is True to terminal
            if debug_log:
                print(
                    f"Agent requested tool calls: {[call.function.name for call in tool_calls]}"
                )

            # Handle Parallel Tool Calls
            for tool_call in tool_calls:
                # Will print log of tool calls if debug_log is True to terminal
                if debug_log:
                    print(
                        f"Processing tool call: {tool_call.function.name} with arguments {tool_call.function.arguments}"
                    )
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Dynamic Dispatch using Function Map
                function_to_call = available_functions.get(function_name)

                if function_to_call:
                    try:
                        tool_result = function_to_call(**function_args)
                    except Exception as e:
                        tool_result = json.dumps({"error": str(e)})
                else:
                    tool_result = json.dumps({"error": "Function not found"})

                # Append RESULT to history
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result,
                    }
                )

            # Second API Call (Get final answer)
            final_response = client.chat.completions.create(
                model="gemini-2.5-flash-lite", messages=messages
            )
            final_content = final_response.choices[0].message.content
            print(f"Agent: {final_content}")
            messages.append({"role": "assistant", "content": final_content})

        else:
            # No tool needed
            print(f"Agent: {response_msg.content}")
            messages.append({"role": "assistant", "content": response_msg.content})


if __name__ == "__main__":
    run_agent()
