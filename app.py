import streamlit as st
import pandas as pd
from collections import Counter
import datetime

# =========================================================
# 🧠 THE MASTER BRAIN: ALL HARDCODED RULES
# =========================================================

# ENGINE 1: EXACT DETERMINISTIC RULES (Includes Numbers & Letters)
EXACT_RULES = {
    # Letter Patterns
    "SSSBSBSBBS": "B",
    "SSBBSBSSBBB": "S",
    "GGRRRGRRRRRG": "G",
    "BRBRBRBGSGSR": "BG",
    "BRSRBGBGSRSRSG": "BG",
    "SGBGSGBRBRBGSGSR": "SG",
    # Number Patterns
    "9955": "6" 
}

# ENGINE 1: REPEATING CYCLE RULES (MODEL 3)
CYCLE_RULES = {
    "GGGRRGGGGG": ["G", "G", "G", "G", "G", "G", "R", "R"],
    "GRRRGGGGRR": ["R", "R", "G", "G", "G", "G", "G", "G"],
    "GRRGGGRRRR": ["R", "G", "G", "G", "R", "G", "R"],
    "BBBSBSSSBBS": ["B", "B", "B", "B", "B", "S"],
    "SBSSSBBBSS": ["B", "B", "S", "B", "S", "B", "B"],
    "RGRGRGGGRG": ["R", "R", "G", "R", "G", "G"]
}

# ENGINE 2: STRUCTURAL RULES (MODEL 2)
STRUCTURAL_RULES = {
    "011010000011": "R",
    "011111101111": "B",
    "000001100101": "R",
    "010000100000": "R"
}

# =========================================================
# ⚙️ LOGIC CORE
# =========================================================

def get_structure(seq):
    mapping = {}
    return "".join([mapping.setdefault(str(x), str(len(mapping))) for x in seq])

def get_predictions(history):
    p1, m1, p2, m2 = None, None, None, None
    
    # Engine 1 Search (Checks Exact and Cycles)
    for length in [12, 11, 10, 8, 7, 6, 4]:
        if len(history) < length: continue
        chunk = "".join(map(str, history[-length:]))
        
        if chunk in EXACT_RULES:
            p1, m1 = EXACT_RULES[chunk], f"Eng 1: Deterministic Match"
            break
        if chunk in CYCLE_RULES:
            cycle = CYCLE_RULES[chunk]
            count = st.session_state.cycle_counts.get(chunk, 0)
            p1, m1 = cycle[count % len(cycle)], f"Eng 1: Cycle Step {count % len(cycle)}"
            break

    # Engine 2 Search (Checks Structure)
    if len(history) >= 12:
        struct = get_structure(history[-12:])
        if struct in STRUCTURAL_RULES:
            p2, m2 = STRUCTURAL_RULES[struct], "Eng 2: Structural Shape AI"
            
    return p1, m1, p2, m2

# =========================================================
# 📱 USER INTERFACE (STREAMLIT)
# =========================================================

st.set_page_config(page_title="2-Engg Master AI", layout="wide")
st.title("🛡️ 2-Engine Master Pattern & Number Tracker")



if 'history' not in st.session_state: st.session_state.history = []
if 'log' not in st.session_state: st.session_state.log = []
if 'cycle_counts' not in st.session_state: st.session_state.cycle_counts = {}

# Sidebar controls
with st.sidebar:
    st.header("Admin Controls")
    if st.button("🗑️ Reset Game History"):
        st.session_state.history, st.session_state.log, st.session_state.cycle_counts = [], [], {}
        st.rerun()

# 1. Prediction Display (Top)
st.divider()
np1, msg1, np2, msg2 = get_predictions(st.session_state.history)

res1, res2 = st.columns(2)
with res1:
    st.metric("Engine 1 (Tracker)", str(np1) if np1 else "---", msg1 if msg1 else "Searching patterns...")
with res2:
    st.metric("Engine 2 (Subber AI)", str(np2) if np2 else "---", msg2 if msg2 else "Analyzing structure...")

# 2. Input Section
st.divider()

# Numeric Input Row
st.subheader("🔢 Input Number Result")
num_cols = st.columns(10)
for i in range(10):
    if num_cols[i].button(str(i), key=f"btn_{i}", use_container_width=True):
        p1, m1, p2, m2 = get_predictions(st.session_state.history)
        
        # Update Cycle Memory
        for length in [10, 11]:
            if len(st.session_state.history) >= length:
                chunk = "".join(map(str, st.session_state.history[-length:]))
                if chunk in CYCLE_RULES:
                    st.session_state.cycle_counts[chunk] = st.session_state.cycle_counts.get(chunk, 0) + 1

        st.session_state.log.append({
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Input": str(i),
            "Eng1_Pred": p1 if p1 else "-",
            "Eng2_Pred": p2 if p2 else "-",
            "Status": "✅" if (str(i) == str(p1) or str(i) == str(p2)) else "❌" if (p1 or p2) else "-"
        })
        st.session_state.history.append(str(i))

# Letter/Category Input Row
st.subheader("🎨 Input Color/Size Result")
cat_cols = st.columns(4)
categories = ["SR", "SG", "BR", "BG"]
for i, cat in enumerate(categories):
    if cat_cols[i].button(cat, key=f"btn_{cat}", use_container_width=True):
        p1, m1, p2, m2 = get_predictions(st.session_state.history)
        
        # Update Cycle Memory
        for length in [10, 11]:
            if len(st.session_state.history) >= length:
                chunk = "".join(map(str, st.session_state.history[-length:]))
                if chunk in CYCLE_RULES:
                    st.session_state.cycle_counts[chunk] = st.session_state.cycle_counts.get(chunk, 0) + 1

        st.session_state.log.append({
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Input": cat,
            "Eng1_Pred": p1 if p1 else "-",
            "Eng2_Pred": p2 if p2 else "-",
            "Status": "✅" if (cat == p1 or cat == p2) else "❌" if (p1 or p2) else "-"
        })
        st.session_state.history.append(cat)

# 3. Log and Download
st.divider()
st.subheader("📊 Streak Tracking Log")
if st.session_state.log:
    log_df = pd.DataFrame(st.session_state.log).iloc[::-1] # Newest first
    st.table(log_df)
    
    csv = pd.DataFrame(st.session_state.log).to_csv(index=False)
    st.download_button("📥 Download History", csv, "streak_results.csv", "text/csv")
