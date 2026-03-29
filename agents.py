import json
from anthropic import Anthropic
from tools import search_web, read_url

client = Anthropic()

TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for a given query. Returns top 5 results with titles, URLs and snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_url",
        "description": "Read the full content of a webpage given its URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to read"
                }
            },
            "required": ["url"]
        }
    }
]

def run_tool(name: str, inputs: dict) -> str:
    if name == "search_web":
        return search_web(inputs["query"])
    elif name == "read_url":
        return read_url(inputs["url"])
    return "Tool not found."

def manager_agent(topic: str) -> list[str]:
    print("\n[Manager] Breaking down topic into sub-questions...")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""You are a research manager. Your job is to break down a research topic 
        into exactly 3 specific sub-questions that when answered together will give a 
        comprehensive understanding of the topic. 
        Respond with ONLY a JSON array of 3 strings. No explanation, no markdown, just the JSON array.
        Example: ["question 1", "question 2", "question 3"]""",
        messages=[{
            "role": "user",
            "content": f"Break this topic into 3 sub-questions: {topic}"
        }]
    )

    raw = response.content[0].text.strip()
    questions = json.loads(raw)
    
    for i, q in enumerate(questions, 1):
        print(f"  Sub-question {i}: {q}")
    
    return questions

def research_agent(question: str) -> str:
    print(f"\n[Researcher] Researching: {question}")

    messages = [{"role": "user", "content": f"Research this question thoroughly: {question}"}]
    max_iterations = 6
    iteration = 0

    while True:
        if iteration >= max_iterations:
            print("  Max iterations reached, moving on.")
            return "Research incomplete due to iteration limit."
        
        iteration += 1
    
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system="""You are a research agent. Follow these steps:
            1. Call search_web ONCE with the question to get the top 5 results.
            2. Call read_url on the 2 most promising URLs
            3. Write a detailed summary of your findings and stop.
            Always use the tools when you need information. Do not guess or make up information.""",
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"  Done researching.")
                    return block.text
            break

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  Using tool: {block.name}")
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})

    return "Research failed."

def writer_agent(topic: str, research_results: list[dict]) -> str:
    print("\n[Writer] Writing final report...")

    research_text = ""
    for i, result in enumerate(research_results, 1):
        research_text += f"RESEARCH {i} — {result['question']}\n"
        research_text += f"{result['findings']}\n\n"

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        system="""You are a professional report writer. Given research findings, 
        write a clear, well-structured report with an introduction, sections for 
        each research finding, and a conclusion. Use plain text, no markdown.""",
        messages=[{
            "role": "user",
            "content": f"Write a comprehensive report on: {topic}\n\nResearch findings:\n{research_text}"
        }]
    )

    return response.content[0].text