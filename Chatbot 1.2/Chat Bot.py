import tkinter as tk
import os

# Fonction pour charger les réponses à partir du fichier "reponses.txt"
def load_responses(file):
    responses = {}
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f:
                key, value = line.strip().split(":")
                responses[key] = value
    return responses

# Fonction pour enregistrer les réponses dans le fichier "reponses.txt"
def save_responses(file, responses):
    with open(file, "w") as f:
        for key, value in responses.items():
            f.write(f"{key}:{value}\n")

# Liste pour stocker les réponses du chat
chat_responses = []

# Fonction pour répondre à une question
def respond(question, responses):
    question = question.lower()
    if question in responses:
        return responses[question]
    else:
        return "Je ne sais pas répondre à cela."

# Fonction pour soumettre une question depuis l'interface
def submit_question(event=None):
    user_input = user_input_entry.get()
    response = respond(user_input, responses)

    # Ajoute la question et la réponse à la liste des réponses du chat
    chat_responses.append(("Vous: " + user_input, "Billy: " + response))

    # Enregistre la nouvelle réponse dans le fichier
    responses[user_input.lower()] = response
    save_responses(response_file, responses)

    # Met à jour la zone de texte du chat
    update_chat_log()

    user_input_entry.delete(0, tk.END)

# Fonction pour proposer une réponse
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

    save_button = tk.Button(propose_window, text="Enregistrer", bg="#28a745", fg="white", font=("Arial", 12), relief=tk.RAISED, command=save_proposed_response)
    save_button.pack()

# Fonction pour mettre à jour la zone de texte du chat
def update_chat_log():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete("1.0", tk.END)  # Efface tout le contenu précédent

    for response in chat_responses:
        chat_log.insert(tk.END, response[0] + "\n", "user")
        chat_log.insert(tk.END, response[1] + "\n", "billy")

    chat_log.config(state=tk.DISABLED)

# Créez la fenêtre principale
window = tk.Tk()
window.title("Chatbot Billy")

# Chargez les réponses depuis le fichier "reponses.txt"
response_file = "reponses.txt"
responses = load_responses(response_file)

# Créez une zone de texte pour afficher le chat
chat_log = tk.Text(window, state=tk.DISABLED, wrap=tk.WORD, font=("Arial", 12), bd=0)
chat_log.pack(expand=True, fill=tk.BOTH, padx=20, pady=5)  # Réduit la marge verticale

chat_log.tag_configure("user", foreground="blue")
chat_log.tag_configure("billy", foreground="green")

# Créez un champ de saisie pour l'utilisateur
user_input_entry = tk.Entry(window, font=("Arial", 12), bd=1, relief=tk.SOLID)
user_input_entry.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
user_input_entry.bind("<Return>", submit_question)  # Permet d'appuyer sur "Entrée" pour envoyer

# Créez un bouton "Envoyer"
submit_button = tk.Button(window, text="Envoyer", bg="#28a745", fg="white", font=("Arial", 12), relief=tk.RAISED, command=submit_question)
submit_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Créez un bouton "Proposer une réponse"
propose_button = tk.Button(window, text="Proposer une réponse", bg="#007bff", fg="white", font=("Arial", 12), relief=tk.RAISED, command=propose_response)
propose_button.pack(pady=10, padx=20, fill=tk.BOTH)

# Configurez l'apparence de la fenêtre
window.geometry("400x600")  # Ajustez la taille de la fenêtre
window.configure(bg="#dedede")  # Définissez la couleur d'arrière-plan

# Mettez à jour la zone de texte du chat avec les réponses chargées depuis le fichier
update_chat_log()

# Exécutez la fenêtre
window.mainloop()
