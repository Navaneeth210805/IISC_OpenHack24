from langchain_community.tools import DuckDuckGoSearchResults
def set_search_query(search_query):
    duck_search_query = search_query
    search = DuckDuckGoSearchResults()
    links = search.run(duck_search_query).split(",")
    urls = []
    for link in links:
        if "link: " in link:
            # print(link)
            url = link.replace("]", "")
            url = url.replace("link: ", "")
            print(url)
            urls.append(url)
    return urls
