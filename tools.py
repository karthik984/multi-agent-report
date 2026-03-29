import requests
from ddgs import DDGS
from bs4 import BeautifulSoup

# def search_web(query: str) -> str:
#     url = "https://duckduckgo.com/html/"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     params = {"q": query}

#     response = requests.get(url, headers=headers, params=params)
#     soup = BeautifulSoup(response.text, "html.parser")

#     results = []
#     for result in soup.select(".result__body")[:5]:
#         title = result.select_one(".result__title")
#         snippet = result.select_one(".result__snippet")
#         link = result.select_one(".result__url")

#         if title and snippet and link:
#             results.append(f"Title: {title.get_text()}\nURL: {link.get_text().strip()}\nSnippet: {snippet.get_text()}")

#     return "\n\n".join(results) if results else "No results found."


def search_web(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    
    if not results:
        return "No results found."
    
    output = ""
    for r in results:
        output += f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n\n"
    
    return output

def read_url(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text[:5000]
