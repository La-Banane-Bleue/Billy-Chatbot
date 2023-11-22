import tkinter as tk
import os
import string

def load_responses(file):
    responses = {}
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f:
                key, value = line.strip().split(":")
                responses[key] = value
    return responses

def save_responses(file, responses):
    with open(file, "w") as f:
        for key, value in responses.items():
            f.write(f"{key}:{value}\n")

def load_settings(file):
    settings = {'Theme': 'Light'}  # Ajout de la clé 'Theme' avec la valeur par défaut
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                settings[key] = value
    return settings

def save_settings(file, settings):
    with open(file, "w") as f:
        for key, value in settings.items():
            f.write(f"{key}={value}\n")

chat_responses = []

def respond(question, responses):
    question = question.lower()

    if "blague" in question:
        print("Bravo, tu as trouvé l'easter egg !")
        return "Ah, tu veux une blague ? Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent toujours dans le bateau !"
    
    translation_table = str.maketrans("", "", string.punctuation.replace("-", ""))
    question = question.translate(translation_table)

    if question[-1] == "?":
        question = question[:-1]

    matching_keys = [key for key in responses.keys() if key.replace("'", "") in question]

    if matching_keys:
        return responses[matching_keys[0]]
    else:
        return "Je ne sais pas répondre à cela."

def submit_question(event=None):
    user_input = user_input_entry.get()

    if "blague" in user_input.lower():
        print("Bravo, tu as trouvé l'easter egg !")

    response = respond(user_input, responses)

    chat_responses.append(("Vous: " + user_input, "Billy: " + response))

    responses[user_input.lower()] = response
    save_responses(response_file, responses)

    update_chat_log()

    user_input_entry.delete(0, tk.END)

def propose_response():
    propose_window = tk.Toplevel(window)
    propose_window.title("Proposer une réponse")

    propose_label = tk.Label(propose_window, text="Nouvelle question et réponse :")
    propose_label.pack()

    propose_question_entry = tk.Entry(propose_window, font=("Arial", 12), bd=1, relief=tk.SOLID)
    propose_question_entry.pack()

    propose_response_entry = tk.Entry(propose_window, font=("Arial", 12), bd=1, relief=tk.SOLID)
    propose_response_entry.pack()

    def save_proposed_response():
        new_question = propose_question_entry.get()
        new_response = propose_response_entry.get()
        responses[new_question.lower()] = new_response
        save_responses(response_file, responses)
        propose_window.destroy()

    save_button = tk.Button(propose_window, text="Enregistrer", bg="#28a745", fg="black", font=("Arial", 12), relief=tk.RAISED, command=save_proposed_response)
    save_button.pack()

def update_chat_log():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete("1.0", tk.END)

    for response in chat_responses:
        chat_log.insert(tk.END, response[0] + "\n", "user")
        chat_log.insert(tk.END, response[1] + "\n", "billy")

    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

def toggle_dark_mode():
    # Inverse l'état du mode sombre et enregistre la valeur dans les paramètres
    settings["Theme"] = "Dark" if settings.get("Theme", "Light") == "Light" else "Light"
    save_settings(settings_file, settings)

    # Met à jour l'apparence en fonction du mode sombre
    update_appearance()

def update_appearance():
    if settings.get("Theme", "Light") == "Dark":
        window.geometry("400x600")  # Ajuste la taille de la fenêtre
        window.configure(bg="#2e2e2e")
        chat_log.config(bg="black", fg="white")
        user_input_entry.config(bg="black", fg="white", insertbackground="white")
    else:
        window.geometry("400x600")  # Ajuste la taille de la fenêtre
        window.configure(bg="#dedede")
        chat_log.config(bg="white", fg="black")
        user_input_entry.config(bg="white", fg="black", insertbackground="black")

# Fonction pour afficher la fenêtre des paramètres
def show_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Paramètres")

    dark_mode_label = tk.Label(settings_window, text="Mode sombre :")
    dark_mode_label.pack()

    dark_mode_checkbox = tk.Checkbutton(settings_window, variable=settings["Theme"], command=toggle_dark_mode)
    dark_mode_checkbox.pack()

# Crée la fenêtre principale
window = tk.Tk()
window.title("Chatbot Billy")

# Charge les réponses depuis le fichier "reponses.txt"
response_file = "reponses.txt"
responses = load_responses(response_file)

# Charge les paramètres depuis le fichier "settings.txt"
settings_file = "settings.txt"
settings = load_settings(settings_file)

# Crée une zone de texte pour afficher le chat
chat_log = tk.Text(window, state=tk.DISABLED, wrap=tk.WORD, font=("Arial", 12), bd=0)
chat_log.pack(expand=True, fill=tk.BOTH, padx=20, pady=5)

chat_log.tag_configure("user", foreground="blue")
chat_log.tag_configure("billy", foreground="green")

# Crée un champ de saisie pour l'utilisateur
user_input_entry = tk.Entry(window, font=("Arial", 12), bd=1, relief=tk.SOLID)
user_input_entry.pack(pady=5, padx=20, fill=tk.BOTH, expand=False)
user_input_entry.bind("<Return>", submit_question)

# Crée un bouton "Envoyer"
submit_button = tk.Button(window, text="Envoyer", bg="#28a745", fg="black", font=("Arial", 12), relief=tk.RAISED, command=submit_question)
submit_button.pack(pady=5, padx=20, fill=tk.BOTH)

# Crée un bouton "Proposer une réponse"
propose_button = tk.Button(window, text="Proposer une réponse", bg="#007bff", fg="black", font=("Arial", 12), relief=tk.RAISED, command=propose_response)
propose_button.pack(pady=5, padx=20, fill=tk.BOTH)

# Crée un bouton "Paramètres"
settings_button = tk.Button(window, text="Paramètres", bg="#ffa600", fg="black", font=("Arial", 12), relief=tk.RAISED, command=show_settings)
settings_button.pack(pady=5, padx=20, fill=tk.BOTH)

# Configure l'apparence de la fenêtre
update_appearance()

# Met à jour la zone de texte du chat avec les réponses chargées depuis le fichier
update_chat_log()

# Exécute la fenêtre
window.mainloop()
