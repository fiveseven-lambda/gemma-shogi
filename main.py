import sys
import ollama

MODEL = "gemma3:1b"


def main():
    while True:
        try:
            info = ollama.show(MODEL)
            print("<!--", info.details, "-->")
            break
        except ollama.ResponseError as e:
            print("<!--", e.error, "-->")
            if e.status_code == 404:
                print("<!-- Downloading", MODEL, "-->")
                ollama.pull(MODEL)
            else:
                sys.exit(1)
    messages = ["""私にひっかけクイズを出してください"""]
    for i, message in enumerate(messages):
        print(f"Initial prompt #{i}:\n")
        print(message)
        print()
    turn = 0
    while True:
        stream = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "user" if i % 2 == turn else "assistant", "content": message}
                for i, message in enumerate(messages)
            ],
            stream=True,
        )
        response = []
        print(f"AI #{turn}:\n")
        for chunk in stream:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
            response.append(content)
        print("\n")
        messages.append("".join(response))
        turn = 1 - turn


if __name__ == "__main__":
    main()
