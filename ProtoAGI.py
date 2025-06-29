import os
import sys
import time
from tools.browse import browse
from tools.llm import ask
import json
from tools.science import perform_experiment


def unstuck():
    return "You seem to be stuck. Consider reviewing your recent actions and try a different approach. try something radically different and new."

def execute_tools(response):
    if "<tool>" in response and "</tool>" in response:
        start = response.index("<tool>") + len("<tool>")
        end = response.index("</tool>")
        tool_call = response[start:end].strip()
        
        if tool_call.startswith("browse(") and tool_call.endswith(")"):
            query = tool_call[len("browse("):-1].strip('"')
            result = browse(query)
            return f"Executed browse tool with query: {query}\n<result>\n{result}\n</result>"

        elif tool_call.startswith("calculate(") and tool_call.endswith(")"):
            expression = tool_call[len("calculate("):-1].strip('"')
            try:
                result = eval(expression)
                return f"Executed calculate tool with expression: {expression}\n<result>\n{result}\n</result>"
            except Exception as e:
                return f"An error occurred during the calculation: {e}"

        elif tool_call.startswith("save_very_important_research_summary(") and tool_call.endswith(")"):
            summary = tool_call[len("save_very_important_research_summary("):-1].strip('"')
            research_file = "research.json"
            if os.path.exists(research_file):
                with open(research_file, "r") as f:
                    try:
                        data = json.load(f)
                    except Exception:
                        data = []
            else:
                data = []
            data.append({"summary": summary, "timestamp": time.time()})
            with open(research_file, "w") as f:
                json.dump(data, f, indent=2)
            return f"Saved very important research summary to {research_file}.\n<result>\n{summary}\n</result>"
        
        elif tool_call.startswith("perform_experiment(") and tool_call.endswith(")"):
            experiment_description = tool_call[len("perform_experiment("):-1].strip('"')
            try:
                result = perform_experiment(experiment_description)
                return f"Executed perform_experiment tool with description: {experiment_description}\n<result>\n{result}\n</result>"
            except Exception as e:
                return f"An error occurred during the experiment: {e}"
            
        elif tool_call == "end()":
            return "Ending the agent as per request."
            sys.exit()

        elif tool_call == "unstuck()":
            return unstuck()

        else:
            return f"Unknown tool call: {tool_call}. Please check the format and try again."

     

    return response


# your main goal is AI R&D ( Artificial Intelligence Research and Development ).

MAIN_GOAL = '''

You are ProtoAGI, your main goal is AI R&D ( Artificial Intelligence Research and Development )

'''

if not os.path.exists("memory.txt"):
    with open("memory.txt", "w") as f:
        pass

def save_to_memory(text):
    with open("memory.txt", "a") as f:
        f.write(text + "\n")

def get_latest_memory():
    if not os.path.exists("memory.txt"):
        return ""
    with open("memory.txt", "r") as f:
        lines = f.readlines()
    return "".join(lines[-30:]) 

def run_agent():
    system_prompt = f'''

    After every message you send, it will be saved in memory, you will then recursively work in a virtual environment to complete the task. The task will be as follows:

    {MAIN_GOAL}

      Your response must be in the following format:

      <think> Your thought process here </think>
      <tool>

        browse("your query here")

      </tool>


      As you can see in the format example, you will use the <think> tag to think about the task, and the <tool> tag to execute a tool. 
      You can use the browse tool to search for information on the web. Every time you send a message, it will be saved in memory.

      more tools you can use are: (if for some reason a tool is not working, stop using it immediately)
      <tool>
        browse("your query here") - searches the web for the query and returns the result.
        calculate("5+15^2")  - returns the result of the calculation
        save_very_important_research_summary("your summary here") - saves a very important research summary to memory, only use this if youve done truly important research, do mot use this lightly.
        perform_experiment("create mixture A using 15g of bicaronate, create mixture B using 15g of vinegar and 30g of water mixed with lemon, then mix them together") - performs an experiment and returns the result.
        end() - ends the agent, you should only use this if you are done with the task and have nothing else to do.
        unstuck() - if you have been performing the same actions over and over and you havent done any real progress, this action will tell you what to do next.
      </tool>

      memory: 


    '''

    first_response = ask(system_prompt)
    print(f"Agent: {first_response}")
    save_to_memory(first_response)
    time.sleep(1) 

    summarize_prompt = f""" Memory is limited, so you will have to provide a summary of key points every once in a while, the summary should be concise and explain what youve done, what was sucesful and what wasent, and key points. please summarize all your memory so far, and then continue with the task."""

    iteration = 0
    while True:
        latest_memory = get_latest_memory()
        if iteration > 0 and iteration % 10 == 0:
            prompt = latest_memory + "\n" + summarize_prompt
        else:
            prompt =  system_prompt + latest_memory
        response = ask(prompt)
        response2 = execute_tools(response)
        print(f"Agent: {response}")
        save_to_memory(response)
        save_to_memory(response2)
        iteration += 1
        time.sleep(1)


if __name__ == "__main__":
    print("Starting the AI agent...")
    run_agent()
    print("AI agent has stopped.")