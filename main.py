from dotenv import load_dotenv
from agents import manager_agent, research_agent, writer_agent

load_dotenv()

def run(topic: str):
    print(f"\nResearch topic: {topic}")
    print("=" * 50)

    questions = manager_agent(topic)

    research_results = []
    for question in questions:
        findings = research_agent(question)
        research_results.append({
            "question": question,
            "findings": findings
        })

    
    report = writer_agent(topic, research_results)

    print("\n" + "=" * 50)
    print("FINAL REPORT")
    print("=" * 50)
    print(report)

    filename = topic.replace(" ", "_")[:30] + ".txt"

    with open(filename, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {filename}")


if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run(topic)
