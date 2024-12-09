import tkinter as tk
import requests
import json
import os
from dotenv import load_dotenv
from tkinter import scrolledtext

load_dotenv()  # Load .env file
api_key = os.getenv('API_KEY')

def fetch_data():
    # Get server name and char name from GUI 
    serverId = serverId_var.get()
    characterName = character_name_entry.get()

    # API Call to get characterID (Needed for another API call)
    getCharacterID = requests.get('https://api.dfoneople.com/df/servers/'+serverId+'/characters?characterName='+ characterName +'&apikey='+ api_key)
    getCharacterID1 = getCharacterID.json()
    characterId = getCharacterID1['rows'][0]['characterId']

    # API Call to get skill build
    url = 'https://api.dfoneople.com/df/servers/'+serverId+'/characters/'+characterId+'/skill/style?apikey='+ api_key
    response = requests.get(url)
        
    if response.status_code == 200:
        # If the request was successful, print the response content
        # Parse JSON response
        data = response.json()
        char_data = f"{data.get('jobName', 'Unknown')} | {data.get('characterName', 'Unknown')} | ({data.get('jobGrowName', 'Unknown')})"
        skill_data = data['skill']
        # Print response 
        response_text.delete(1.0, tk.END)
        response_text.insert(tk.END, json.dumps(char_data, indent=3))
        response_text.insert(tk.END, json.dumps(skill_data, indent=3))
    else:
        # If there was an error, print the status code and reason
        response_text.delete(1.0, tk.END)
        response_text.insert(tk.END, f"Error: {response.status_code} - {response.reason}")


# Create GUI
root = tk.Tk()
root.title("API GUI")

# Server Name
server_names = ['cain', 'sirocco']  
serverId_label = tk.Label(root, text="Server Name:")
serverId_label.grid(row=0, column=0)
serverId_var = tk.StringVar(root)
serverId_var.set(server_names[0]) 
serverId_dropdown = tk.OptionMenu(root, serverId_var, *server_names)
serverId_dropdown.grid(row=0, column=1)

# Character Name
character_name_label = tk.Label(root, text="Character Name:")
character_name_label.grid(row=3, column=0)
character_name_entry = tk.Entry(root)
character_name_entry.grid(row=3, column=1)

# Button to Fetch Data
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=4, column=0, columnspan=2)

# Text area to display response
response_text = scrolledtext.ScrolledText(root, height=40, width=90, wrap=tk.WORD)
response_text.grid(row=5, column=0, columnspan=2)

root.mainloop()

