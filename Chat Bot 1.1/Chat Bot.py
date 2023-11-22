import tkinter as tk
import os

# Fonction pour charger les réponses personnalisées à partir du fichier.
def load_responses(file):
    responses = {}
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f:
                key, value = line.strip().split(":")
                responses[key] = value
    return responses

# Fonction pour enregistrer les réponses personnalisées dans le fichier.
def save_responses(file, responses):
    with open(file, "w") as f:
        for key, value in responses.items():
            f.write(f"{key}:{value}\n")

# Fonction pour répondre à une question.
def respond(question, responses):
    question = question.lower()
    if question in responses:
        return responses[question]
    else:
        return "Je ne sais pas répondre à cela."

# Fonction pour soumettre une question depuis l'interface.
def submit_question(event=None):
    user_input = user_input_entry.get()
    response = respond(user_input, responses)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Vous: " + user_input + "\n", "user")
    chat_log.insert(tk.END, "Billy: " + response + "\n", "billy")
    chat_log.config(state=tk.DISABLED)
    user_input_entry.delete(0, tk.END)

# Fonction pour ouvrir la fenêtre de proposition de réponses
def open_propose_window():
    propose_window = tk.Toplevel(window)
    propose_window.title("Proposer une réponse")

    propose_label = tk.Label(propose_window, text="Nouvelle question et réponse :")
    propose_label.pack()

    propose_question_entry = tk.Entry(propose_window)
    propose_question_entry.pack()

    propose_response_entry = tk.Entry(propose_window)
    propose_response_entry.pack()

    def save_proposed_response():
        new_question = propose_question_entry.get()
        new_response = propose_response_entry.get()
        responses[new_question.lower()] = new_response
        save_responses(response_file, responses)
        propose_window.destroy()

    save_button = tk.Button(propose_window, text="Enregistrer", command=save_proposed_response)
    save_button.pack()

# Créez la fenêtre principale
window = tk.Tk()
window.title("Chatbot Billy")

# Chargez les réponses personnalisées depuis le fichier
response_file = "reponses.txt"
responses = load_responses(response_file)

# Créez un bouton "Proposer"
propose_button = tk.Button(window, text="Proposer une réponse", command=open_propose_window)
propose_button.pack()

# Créez un champ de saisie pour l'utilisateur
user_input_label = tk.Label(window, text="Vous:")
user_input_label.pack()
user_input_entry = tk.Entry(window)
user_input_entry.pack()
user_input_entry.bind("<Return>", submit_question)  # Permet d'appuyer sur "Entrée" pour envoyer

# Créez un bouton "Envoyer"
submit_button = tk.Button(window, text="Envoyer", command=submit_question)
submit_button.pack()

# Créez une zone de texte pour afficher le chat
chat_log = tk.Text(window, state=tk.DISABLED)
chat_log.pack()
chat_log.tag_configure("user", foreground="blue")
chat_log.tag_configure("billy", foreground="green")

# Exécutez la fenêtre
window.mainloop()
