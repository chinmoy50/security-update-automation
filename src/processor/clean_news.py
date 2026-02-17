def clean_news(news_items):
    cleaned = []

    for item in news_items:
        content = item["content"].strip()
        content = " ".join(content.split())

        cleaned.append({
            "source": item["source"],
            "content": content
        })

    return cleaned