import requests
from urllib.parse import quote

def web_search(query, max_results=5):
    try:
        url = "https://html.duckduckgo.com/html/?q=" + quote(query)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")

        results = []

        for item in soup.select(".result")[:max_results]:
            title = item.select_one(".result__title")
            link = item.select_one(".result__a")
            snippet = item.select_one(".result__snippet")

            if title and link:
                results.append({
                    "title": title.get_text(" ", strip=True),
                    "url": link.get("href"),
                    "snippet": snippet.get_text(" ", strip=True) if snippet else ""
                })

        return results

    except Exception as e:
        return [{"error": str(e)}]
