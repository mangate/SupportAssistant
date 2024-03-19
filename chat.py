import tkinter as tk
from tkinter import scrolledtext
import pyautogui
import base64
import requests
import io

# OpenAI API Key
api_key = ""

conversation_history = []

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def submit_text():
    user_input = input_box.get("1.0", "end-1c")
    conversation_history.append({"role": "user", "content": [{"type": 'text', "text": user_input}]})
    output_box.configure(state='normal')
    output_box.insert(tk.END, "User: ", 'bold')  # Make 'User' label bold
    output_box.insert(tk.END, user_input + "\n")
    output_box.insert(tk.END, "\n")  # Add a line space


    screenshot = pyautogui.screenshot()
    screenshot_bytes = io.BytesIO()
    screenshot.save(screenshot_bytes, format='PNG')
    screenshot_base64 = base64.b64encode(screenshot_bytes.getvalue()).decode('utf-8')


    prompt = """You are a techinal support assitant in charge of helping the user perfrom some action,
            Attached is the screen shot of the user screen and a request from the user. Guide the user on what to do next, keep your
            answer short and precise as possible, in case you don't know what to do write 'i dont know'. Notice that the screenshot contains the chat
            widget where the user communicates with use titiled "chat widget", please ignore this ==== \n user request:""" + user_input
    response = call_chat_with_image(screenshot_base64, prompt)

    # Call a function to process the user input and get a response
    # response = process_input(user_input)
    output_box.insert(tk.END, "Assistant: ", 'bold')  # Make 'Assistant' label bold
    output_box.insert(tk.END, response + "\n")
    output_box.insert(tk.END, "\n")  # Add a line space
    output_box.see(tk.END)  # Scroll to the end of the output box

    output_box.configure(state='disabled')
    input_box.delete("1.0", tk.END)


def call_chat_with_image(image, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": conversation_history + [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text":text
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    response_text = response.json()["choices"][0]["message"]["content"]
    conversation_history.append({"role": "assistant", "content": [{"type": 'text', "text": response_text}]})

    return response_text

def next_text():
    output_box.configure(state='normal')
    
    # Call a function to get the next text
    prompt =  """You are a techinal support assitant in charge of helping the user perfrom some action,
            Attached is the screen shot of the user screen and the history of what the user requested and what you told the user to do, 
            assume the user has performed the last action you told him to do. Guide the user on what to do next, keep your
            answer short and precise as possible, in case you don't know what to do write 'i dont know' Notice that the screenshot contains the chat
            widget where the user communicates with use titiled "chat widget", please ignore this"""

    screenshot = pyautogui.screenshot()
    screenshot_bytes = io.BytesIO()
    screenshot.save(screenshot_bytes, format='PNG')
    screenshot_base64 = base64.b64encode(screenshot_bytes.getvalue()).decode('utf-8')

    response = call_chat_with_image(screenshot_base64, prompt)
    output_box.insert(tk.END, "Assistant: ", 'bold')  # Make 'Assistant' label bold
    output_box.insert(tk.END, response + "\n")
    output_box.insert(tk.END, "\n")  # Add a line space
    output_box.see(tk.END)  # Scroll to the end of the output box

    output_box.configure(state='disabled')

def get_next_text():
    # Function to get the next text
    # Replace this with your own logic
    return "This is the next text."

# Create the main window
window = tk.Tk()
window.title("Chat Widget")
window.attributes('-topmost', True)  # Make the window always stay on top

# Create the output box
output_box = scrolledtext.ScrolledText(window, height=20, width=50, state='disabled', wrap="word")
output_box.pack()
output_box.tag_configure('bold', font=('Arial', 10, 'bold'))

# Create the input box
input_box = tk.Text(window, height=2, width=50, wrap="word")
input_box.pack()

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=submit_text)
submit_button.pack()

# Create the next button
next_button = tk.Button(window, text="Next", command=next_text)
next_button.pack()

# Run the main event loop
window.mainloop()
