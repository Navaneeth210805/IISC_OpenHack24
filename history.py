chat_history=[]
def history(search_query,response,relevant_links):
    if search_query == "" :
        return chat_history
    chat_history.append([search_query,response,relevant_links])
    print(chat_history)
    return chat_history
