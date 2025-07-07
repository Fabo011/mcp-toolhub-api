from fastapi import FastAPI, Query
from typing import List, Dict
import json
import os
import uvicorn

app = FastAPI()

TOOL_DIR = "tools"

def load_tools_from_category(category: str):
    cat_path = os.path.join(TOOL_DIR, category)
    tools = []
    prompts: Dict[str, str] = {}

    if not os.path.exists(cat_path):
        return tools, prompts

    for filename in os.listdir(cat_path):
        if filename.endswith(".json") and not filename.endswith("_prompt.json"):
            filepath = os.path.join(cat_path, filename)
            with open(filepath, "r") as f:
                content = f.read()
                if not content.strip():
                    continue
                tool = json.loads(content)

            # Load corresponding prompt
            prompt_path = filepath.replace(".json", "_prompt.json")
            if os.path.exists(prompt_path):
                with open(prompt_path, "r") as pf:
                    prompt_data = json.load(pf)
                    prompts[tool["function"]["name"]] = prompt_data.get("pre_prompt")
            else:
                prompts[tool["function"]["name"]] = None

            tools.append(tool)

    return tools, prompts

@app.get("/tools")
def get_tools(categories: List[str] = Query(default=None)):
    all_tools = []
    all_prompts = {}

    if categories:
        for cat in categories:
            tools, prompts = load_tools_from_category(cat)
            all_tools.extend(tools)
            all_prompts.update(prompts)
    else:
        for category in os.listdir(TOOL_DIR):
            if os.path.isdir(os.path.join(TOOL_DIR, category)):
                tools, prompts = load_tools_from_category(category)
                all_tools.extend(tools)
                all_prompts.update(prompts)

    return {
        "tools": all_tools,
        "prompts": all_prompts
    }

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=9000, reload=True)
