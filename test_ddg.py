from DDG_handler import duckduckgo_search

if __name__ == "__main__":
    query = "Какая погода в Москве сегодня?"
    print("Отправляю запрос в DuckDuckGo...")
    results = duckduckgo_search(query)
    print("\nРезультаты поиска:")

    if isinstance(results, str):
        print("Ошибка или сообщение:", results)
    else:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}: {result['body']} ({result['href']})")