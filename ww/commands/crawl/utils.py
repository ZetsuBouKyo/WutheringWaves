def clear_text(text: str) -> str:
    text_list = text.split("\n")
    while len(text_list) > 0 and text_list[-1] == "":
        text_list.pop()
    for i in range(len(text_list)):
        text_list[i] = text_list[i].strip()
    text = "\n".join(text_list)
    return text
