# Multi-Agent Report Generator

A multi-agent research system that generates comprehensive reports on any topic. Three specialized AI agents collaborate — a manager breaks down the topic, researchers gather information from the web, and a writer produces the final report.

## How it works

```
Manager Agent    → breaks topic into 3 focused sub-questions
Researcher Agent → searches the web and reads pages for each sub-question (runs 3 times)
Writer Agent     → synthesizes all research into a structured report
```

Each agent has a specific role and system prompt. No single agent does everything — they hand off work to each other through main.py.

## Tech stack

- **[Claude Haiku](https://www.anthropic.com/)** — all three agents powered by claude-haiku-4-5
- **[duckduckgo-search](https://github.com/deedy5/duckduckgo_search)** — web search tool
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** — webpage content extraction

## Project structure

```
multi-agent-report/
├── .env                  # API key (not committed)
├── .env.example          # Template for .env
├── requirements.txt
├── tools.py              # search_web and read_url functions
├── agents.py             # manager, researcher, and writer agents
└── main.py               # orchestrates the three agents
```

## Setup

**1. Clone the repo and create a virtual environment**

```bash
git clone https://github.com/karthik984/multi-agent-report.git
cd multi-agent-report
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

**2. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**3. Add your Anthropic API key**

```
ANTHROPIC_API_KEY=sk-ant-yourkey
```

**4. Run the agent**

```bash
python main.py
```

## Example

```
Enter research topic: Porsche 911

[Manager] Breaking down topic into sub-questions...
  Sub-question 1: What are the key design features across generations?
  Sub-question 2: How has engine technology evolved since 1963?
  Sub-question 3: What is its cultural significance in automotive history?

[Researcher] Researching: What are the key design features...
  Using tool: search_web
  Using tool: read_url
  Done researching.

[Writer] Writing final report...

FINAL REPORT
...
```

## Key concepts demonstrated

- Multi-agent architecture with specialized roles
- Agent loop pattern with tool use
- Passing research results between agents
- Max iteration limits to prevent infinite loops
- Cheap model (Haiku) for all agents to minimize API costs