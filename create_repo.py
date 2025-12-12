#!/usr/bin/env python3
"""Script pour créer automatiquement le dépôt GitHub et pousser le code."""
import os
import subprocess
import sys
import json

USERNAME = "jack"
REPO_NAME = "pioneer_avr_lx83"
REPO_DESCRIPTION = "Home Assistant integration for Pioneer AVR LX83"

def get_github_token():
    """Essayer de récupérer le token GitHub depuis différentes sources."""
    # 1. Variable d'environnement
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    
    # 2. Fichier de configuration local
    config_file = os.path.expanduser("~/.github_token")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            token = f.read().strip()
            if token:
                return token
    
    return None

def create_repo(token):
    """Créer le dépôt sur GitHub via l'API."""
    import urllib.request
    import urllib.error
    
    url = "https://api.github.com/user/repos"
    data = json.dumps({
        "name": REPO_NAME,
        "description": REPO_DESCRIPTION,
        "private": False,
        "auto_init": False
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                print("✅ Dépôt créé avec succès!")
                return True
            elif response.status == 422:
                print("ℹ️  Le dépôt existe déjà, c'est parfait!")
                return True
            else:
                body = response.read().decode()
                print(f"❌ Erreur: {response.status}")
                print(body)
                return False
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Erreur d'authentification. Token invalide.")
        elif e.code == 422:
            print("ℹ️  Le dépôt existe déjà, c'est parfait!")
            return True
        else:
            print(f"❌ Erreur HTTP {e.code}: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def setup_remote():
    """Configurer le remote Git."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Remote déjà configuré")
            return True
    except:
        pass
    
    print("➕ Configuration du remote...")
    result = subprocess.run(
        ["git", "remote", "add", "origin", f"https://github.com/{USERNAME}/{REPO_NAME}.git"],
        capture_output=True
    )
    return result.returncode == 0

def push_code():
    """Pousser le code vers GitHub."""
    print("\n📤 Poussage du code vers GitHub...")
    result = subprocess.run(["git", "push", "-u", "origin", "main"])
    return result.returncode == 0

def main():
    print("🚀 Création automatique du dépôt GitHub...\n")
    
    # Récupérer le token
    token = get_github_token()
    if not token:
        print("⚠️  Token GitHub non trouvé.")
        print("\nPour créer le dépôt automatiquement:")
        print("1. Créez un Personal Access Token sur: https://github.com/settings/tokens")
        print("2. Cochez 'repo' (toutes les permissions)")
        print("3. Exécutez une des commandes suivantes:")
        print("   export GITHUB_TOKEN='votre_token'")
        print("   # OU")
        print(f"   echo 'votre_token' > ~/.github_token")
        print("\nEnsuite, relancez ce script.")
        print("\nOu créez le dépôt manuellement sur: https://github.com/new")
        print(f"Puis exécutez: git push -u origin main")
        sys.exit(1)
    
    # Créer le dépôt
    if not create_repo(token):
        sys.exit(1)
    
    # Configurer le remote
    if not setup_remote():
        print("❌ Erreur lors de la configuration du remote")
        sys.exit(1)
    
    # Pousser le code
    if push_code():
        print("\n✅ Succès! Votre code est maintenant sur GitHub:")
        print(f"   https://github.com/{USERNAME}/{REPO_NAME}")
        print("\n🎉 Prochaines étapes:")
        print("   1. Allez sur votre dépôt GitHub")
        print("   2. Créez une release v1.0.0")
        print("   3. Partagez le lien avec la communauté Home Assistant!")
    else:
        print("\n❌ Erreur lors du push.")
        print("   Vérifiez vos permissions et votre authentification Git.")

if __name__ == "__main__":
    main()

