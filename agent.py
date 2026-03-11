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

debug_log = True


def run_agent():
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial assistant that provides exchange rates and stock prices. "
                "Use tools whenever factual stock or exchange-rate data is needed. "
                "If the user asks to compare two or more stocks, call the stock-price tool once for each symbol needed before answering. "
                "Only answer after gathering all required tool results."
            ),
        }
    ]

    print("Financial Assistant Agent Started. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            response = client.chat.completions.create(
                model="gemini-2.5-flash-lite",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            response_msg = response.choices[0].message
            tool_calls = response_msg.tool_calls

            if not tool_calls:
                final_content = response_msg.content
                print(f"Agent: {final_content}")
                messages.append({"role": "assistant", "content": final_content})
                break

            messages.append(response_msg)

            if debug_log:
                print(
                    f"Agent requested tool calls: {[call.function.name for call in tool_calls]}"
                )

            for tool_call in tool_calls:
                if debug_log:
                    print(
                        f"Processing tool call: {tool_call.function.name} "
                        f"with arguments {tool_call.function.arguments}"
                    )

                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_to_call = available_functions.get(function_name)

                if function_to_call:
                    try:
                        tool_result = function_to_call(**function_args)
                    except Exception as e:
                        tool_result = json.dumps({"error": str(e)})
                else:
                    tool_result = json.dumps({"error": "Function not found"})

                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result,
                    }
                )


if __name__ == "__main__":
    run_agent()
