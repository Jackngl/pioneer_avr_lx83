#!/usr/bin/env python3
"""Test script pour vérifier le code retourné par THX Cinema."""

import socket
import time

HOST = "192.168.1.26"
PORT = 23
TIMEOUT = 5

def send_command(command):
    """Envoie une commande Telnet et retourne la réponse."""
    try:
        sock = socket.create_connection((HOST, PORT), timeout=TIMEOUT)
        sock.settimeout(TIMEOUT)
        
        # Envoyer la commande
        cmd_bytes = (command + "\r").encode()
        sock.sendall(cmd_bytes)
        time.sleep(0.5)  # Attendre la réponse
        
        # Lire la réponse
        response = b""
        try:
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                response += chunk
                if b"\r" in response or b"\n" in response:
                    break
        except socket.timeout:
            pass
        
        sock.close()
        return response.decode('utf-8', errors='ignore').strip()
    except Exception as e:
        return f"Erreur: {e}"

def main():
    print("=" * 70)
    print("Test THX Cinema - Codes retournés par l'amplificateur")
    print("=" * 70)
    print()
    
    # 1. Vérifier l'état actuel
    print("1. Mode d'écoute actuel:")
    current = send_command("?L")
    print(f"   Réponse: {repr(current)}")
    print()
    
    # 2. Sélectionner THX Cinema (code correct: 0101SR)
    print("2. Sélection de THX Cinema (0101SR - code correct):")
    result = send_command("0101SR")
    print(f"   Réponse: {repr(result)}")
    time.sleep(1.5)  # Attendre que l'amplificateur change de mode
    print()
    
    # 3. Interroger à nouveau
    print("3. Mode d'écoute après sélection (?L):")
    after = send_command("?L")
    print(f"   Réponse: {repr(after)}")
    print()
    
    # 4. Analyser la réponse
    print("4. Analyse:")
    if "LM" in after:
        lm_index = after.find("LM")
        after_lm = after[lm_index + 2:]
        digits = "".join(ch for ch in after_lm if ch.isdigit())
        print(f"   Code extrait: {repr(digits)}")
        if len(digits) >= 4:
            code_4 = digits[:4].zfill(4)
            print(f"   Code 4 chiffres: {code_4}")
            if code_4 == "0101":
                print(f"   ✓✓✓ Code correct pour THX Cinema!")
            else:
                print(f"   ⚠ Code différent de 0101 - à vérifier")
        if len(digits) >= 2:
            code_2 = digits[-2:]
            print(f"   2 derniers chiffres: {code_2}")
    else:
        digits = "".join(ch for ch in after if ch.isdigit())
        print(f"   Chiffres trouvés: {repr(digits)}")
    
    print()
    print("=" * 70)
    print("Codes THX corrects:")
    print("  0101SR = THX Cinema")
    print("  0102SR = THX Music")
    print("  0103SR = THX Games")
    print("  0115SR = THX Surround EX")
    print("  0105SR = THX Select2 Cinema")
    print("  0106SR = THX Select2 Music")
    print("  0107SR = THX Select2 Games")
    print("=" * 70)

if __name__ == "__main__":
    main()

