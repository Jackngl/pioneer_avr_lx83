import socket
import time

def send_and_read(s, cmd):
    """Envoie une commande et lit toutes les réponses."""
    s.sendall(f"{cmd}\r".encode())
    time.sleep(0.5)
    responses = []
    while True:
        try:
            s.settimeout(0.8)
            data = s.recv(1024).decode().strip()
            if data:
                for line in data.split('\r\n'):
                    line = line.strip()
                    if line:
                        responses.append(line)
        except socket.timeout:
            break
    return responses

def get_lm(responses):
    """Extrait le dernier code LM des réponses."""
    lm = None
    for r in responses:
        if r.startswith("LM"):
            lm = r[2:]
    return lm

def test_cycle(s, name, code, times):
    """Envoie la même commande N fois pour tester le cycle."""
    print(f"\n{'='*55}")
    print(f"CYCLE TEST: {name} ({code}SR x{times})")
    print(f"{'='*55}")
    results = []
    for i in range(times):
        responses = send_and_read(s, f"{code}SR")
        lm = get_lm(responses)
        status = f"LM={lm}" if lm else "No LM"
        print(f"  Appui {i+1}: {status}")
        results.append(lm)
        time.sleep(0.5)
    return results

def test_thx_after_dolby(s, dolby_name, dolby_code, thx_name, thx_code):
    """Active d'abord un mode Dolby, puis teste le THX."""
    print(f"\n{'='*55}")
    print(f"THX TEST: {dolby_name} -> {thx_name}")
    print(f"{'='*55}")
    
    # 1. Activer le mode Dolby
    responses = send_and_read(s, f"{dolby_code}SR")
    lm = get_lm(responses)
    print(f"  1. {dolby_name} ({dolby_code}SR): LM={lm}")
    time.sleep(0.5)
    
    # 2. Activer le THX par-dessus
    responses = send_and_read(s, f"{thx_code}SR")
    lm = get_lm(responses)
    print(f"  2. {thx_name} ({thx_code}SR): LM={lm}")
    time.sleep(0.5)
    
    return lm

def main():
    host = "192.168.1.26"
    port = 8102
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Connected to {host}:{port}")
            time.sleep(0.5)
            
            # Vérifier power
            pwr = send_and_read(s, "?P")
            print(f"Power: {pwr}")
            if any("PWR1" in r for r in pwr):
                print("AVR OFF, turning ON...")
                send_and_read(s, "PO")
                time.sleep(8)
            
            # =============================================
            # TEST 1: Cycle STÉRÉO (0001SR x5)
            # =============================================
            stereo_results = test_cycle(s, "Stéréo", "0001", 5)
            
            # =============================================
            # TEST 2: Cycle STANDARD (0010SR x5)
            # =============================================
            standard_results = test_cycle(s, "Standard/Dolby", "0010", 7)
            
            # =============================================
            # TEST 3: Cycle DSP (0100SR x5)
            # =============================================
            dsp_results = test_cycle(s, "DSP/Advanced", "0100", 5)
            
            # =============================================
            # TEST 4: THX Select2 après Dolby PLII Movie
            # =============================================
            # D'abord mettre en PLII Movie
            test_thx_after_dolby(s, "PLII Movie", "0013", "THX Select2 Cinema", "0054")
            test_thx_after_dolby(s, "PLII Movie", "0013", "THX Select2 Music", "0055")
            test_thx_after_dolby(s, "PLII Movie", "0013", "THX Select2 Games", "0056")
            test_thx_after_dolby(s, "PLII Movie", "0013", "THX Surround EX", "0057")
            
            # =============================================
            # TEST 5: THX Select2 après Neo:6
            # =============================================
            test_thx_after_dolby(s, "Neo:6 Music", "0012", "THX Select2 Cinema", "0054")
            
            # =============================================
            # TEST 6: Cycle THX (0050SR)
            # =============================================
            # D'abord activer un mode Dolby
            send_and_read(s, "0013SR")
            time.sleep(0.5)
            thx_cycle = test_cycle(s, "THX Cycle (après Dolby)", "0050", 7)
            
            # =============================================
            # TEST 7: Neo:6 Cinema (0011SR) - après reset
            # =============================================
            print(f"\n{'='*55}")
            print(f"TEST: Neo:6 Cinema (0011SR)")
            print(f"{'='*55}")
            # Reset en stereo d'abord
            send_and_read(s, "0001SR")
            time.sleep(1)
            responses = send_and_read(s, "0011SR")
            lm = get_lm(responses)
            print(f"  Neo:6 Cinema: LM={lm}")
            
            # =============================================
            # TEST 8: Action (0101SR) - retry
            # =============================================
            print(f"\n{'='*55}")
            print(f"TEST: Action (0101SR) - retry")
            print(f"{'='*55}")
            send_and_read(s, "0001SR")
            time.sleep(1)
            responses = send_and_read(s, "0101SR")
            lm = get_lm(responses)
            print(f"  Action: LM={lm}")
            
            # =============================================
            # TEST 9: Rock/Pop (0108SR) - retry
            # =============================================
            print(f"\n{'='*55}")
            print(f"TEST: Rock/Pop (0108SR) - retry")
            print(f"{'='*55}")
            send_and_read(s, "0001SR")
            time.sleep(1)
            responses = send_and_read(s, "0108SR")
            lm = get_lm(responses)
            print(f"  Rock/Pop: LM={lm}")
            
            # Remettre en Stereo
            send_and_read(s, "0001SR")
            print("\n\n✅ Tests terminés. Ampli remis en Stereo.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
