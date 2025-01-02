from duckduckgo_search import DDGS

def duckduckgo_search(query: str, max_results: int = 3):
    try:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": result.get("title", "Без названия"),
                    "body": result.get("body", "Описание отсутствует"),
                    "href": result.get("href", "")
                })
        if not results:
            return "По вашему запросу ничего не найдено."
        return results
    except Exception as e:
        return f"Ошибка при поиске через DuckDuckGo: {e}"


