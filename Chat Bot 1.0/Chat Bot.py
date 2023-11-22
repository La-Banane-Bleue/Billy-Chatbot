import os

# Définissez le chemin du fichier de réponses personnalisées.
response_file = "reponses.txt"

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

responses = load_responses(response_file)

while True:
    user_input = input("Vous: ")
    if user_input.lower() == "quitter":
        break
    elif user_input.lower() == "enregistrer":
        question = input("Entrez la question : ")
        answer = input("Entrez la réponse : ")
        responses[question.lower()] = answer
        save_responses(response_file, responses)
        print("Réponse enregistrée.")
    elif user_input.lower() == "modifier":
        question_to_modify = input("Entrez la question que vous souhaitez modifier : ")
        if question_to_modify.lower() in responses:
            new_answer = input("Entrez la nouvelle réponse : ")
            responses[question_to_modify.lower()] = new_answer
            save_responses(response_file, responses)
            print("Réponse modifiée.")
        else:
            print("La question n'existe pas dans les réponses enregistrées.")
    else:
        response = respond(user_input, responses)
        print("Chatbot:", response)
