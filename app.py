import pandas as pd

# Load the pattern database
df = pd.read_csv('deterministic_patterns_full_analysis.csv')

# Ensure we only use 100% accurate patterns for "100% results"
perfect_patterns = df[df['Accuracy %'] == 100.0].copy()

def get_properties(val):
    """Maps a number or character to Big/Small and Red/Green."""
    if val in ['B', 'S', 'R', 'G', 'SR', 'SG', 'BR', 'BG']:
        # If result is already a category
        mapping = {
            'B': 'BIG', 'S': 'SMALL', 
            'R': 'RED', 'G': 'GREEN',
            'SR': 'SMALL RED', 'SG': 'SMALL GREEN',
            'BR': 'BIG RED', 'BG': 'BIG GREEN'
        }
        return mapping.get(val, val)
    
    try:
        n = int(val)
        size = "BIG" if n >= 5 else "SMALL"
        color = "RED" if n % 2 == 0 else "GREEN"
        return f"{n} {size} {color}"
    except:
        return val

def translate_history(history_str):
    """Converts numeric history into S/B and R/G strings for matching."""
    sb = "".join(['B' if int(n) >= 5 else 'S' for n in history_str])
    rg = "".join(['R' if int(n) % 2 == 0 else 'G' for n in history_str])
    return sb, rg

def find_prediction(history):
    sb_hist, rg_hist = translate_history(history)
    best_match = None

    # Search for the longest 100% accurate match
    for _, row in perfect_patterns.iterrows():
        pattern = str(row['Pattern'])
        stream = row['Stream']
        
        # Determine which history string to check against
        if stream == 'S/B':
            target = sb_hist
        elif stream == 'R/G':
            target = rg_hist
        else:
            target = history # Numbers or Combined

        if target.endswith(pattern):
            if best_match is None or len(pattern) > len(best_match['Pattern']):
                best_match = row

    if best_match is not None:
        next_res = str(best_match['Next result'])
        # Handle cycle results like "4 -> 3"
        prediction = next_res.split('->')[0].strip()
        
        print("\n=== 100% ACCURACY PREDICTION ===")
        print(f"RESULT: {get_properties(prediction)}")
        print("-" * 30)
        print(f"Model: {best_match['Model']}")
        print(f"Pattern: {best_match['Pattern']}")
        print(f"Length: {best_match['Length']}")
        print(f"Occurrence: {best_match['Occurrence count']}")
        print(f"Next Raw: {best_match['Next result']}")
        print(f"Accuracy: {best_match['Accuracy %']}%")
        print("=" * 30)
    else:
        print("\n[!] No 100% match found in database for this sequence.")

# --- LIVE TEST ---
# 1. Provide your initial history (5-6 digits)
user_history = input("Enter current game history (e.g., 9955): ")

# 2. Run the engine
find_prediction(user_history)
