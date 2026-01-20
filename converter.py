import json
import os

filename = "clebottest.json"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        try:
            # Charge le JSON pour s'assurer qu'il est valide
            data = json.load(f)
            
            # Convertit le dictionnaire en une chaîne JSON compacte (sans espaces)
            # separators=(',', ':') permet d'enlever les espaces après les virgules et deux-points
            json_compact = json.dumps(data, separators=(',', ':'))
            
            print("\n✅ Voici la ligne à copier dans ton fichier .env :\n")
            # On utilise des guillemets simples autour du JSON pour éviter les conflits
            print(f"GOOGLE_SHEETS_CREDENTIALS='{json_compact}'")
            print("\n")
            
        except json.JSONDecodeError:
            print(f"❌ Erreur : Le fichier {filename} ne contient pas du JSON valide.")
else:
    print(f"❌ Erreur : Le fichier {filename} n'a pas été trouvé dans ce dossier.")
