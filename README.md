# BoTravel

Ce programme est un chatbot conçu pour aider les utilisateurs à trouver des hôtels. Il est basé sur la bibliothèque streamlit, qui permet la création d'interfaces web pour les applications de science des données.

Le chatbot utilise un modèle Spacy, en_core_web_sm, pour effectuer une analyse sémantique des requêtes des utilisateurs. Il utilise également un ensemble de données, stocké dans le fichier CSV Hotel_Chatbot.csv, pour recommander des hôtels en fonction des critères de recherche des utilisateurs.

Le fichier CSV Hotel_Chatbot.csv est importé à l'aide de la fonction import_dataset(), qui lit le fichier CSV et pré-traite les données en éliminant les colonnes inutiles et les lignes contenant des valeurs manquantes. La fonction renvoie ensuite le DataFrame traité.

Le modèle Spacy est chargé à l'aide de la fonction spacy_model(). Cette fonction renvoie le modèle Spacy en_core_web_sm.

La fonction get_amenities() est utilisée pour extraire les commodités demandées par l'utilisateur à partir de la requête entrée. Elle retourne deux valeurs : une indiquant si des commodités ont été demandées pour la chambre, l'autre indiquant si des commodités communes à l'hôtel ont été demandées.

La fonction get_features() est utilisée pour extraire les informations de recherche des utilisateurs à partir de leur requête. Elle prend en entrée la ville, la région, le prix, la plage de prix et la requête de l'utilisateur. Elle renvoie ces informations mises à jour en fonction de la requête.

La fonction recommend_hotels() est utilisée pour recommander des hôtels en fonction des critères de recherche des utilisateurs. Elle prend en entrée le DataFrame pré-traité, la ville, la région, le prix et la plage de prix et renvoie les hôtels correspondants.

Enfin, les fonctions greeting_inputs_start et greeting_responses_start sont utilisées pour générer des salutations aléatoires pour le chatbot.
