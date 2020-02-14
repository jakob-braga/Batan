def split_text(text):
    i = 0
    last_space = 0
    low = []
    for char in text:
        if last_space == 0 and char == " ":
            low.append(text[last_space:i + 1])
            last_space = i
        elif char == " ":
            low.append(text[last_space + 1:i + 1])
            last_space = i
        elif i == len(text) - 1:
            low.append(text[last_space + 1:])
        i += 1
    return low


def back_to_text(low):
    text = ""
    for word in low:
        text = text + word
    return text