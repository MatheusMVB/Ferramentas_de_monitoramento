import pandas as pd
import re
from collections import defaultdict

# --- 1. Ler CSV da aplicação ---
df = pd.read_csv("offloading (3).csv")

# --- 2. Extrair HH:MM:SS do campo textual de timestamp ---
def extrai_segundo(ts):
    if not isinstance(ts, str):
        return None
    m = re.search(r"(\d{2}:\d{2}:\d{2})", ts)
    return m.group(1) if m else None

df["second"] = df["time"].apply(extrai_segundo)
df = df.dropna(subset=["second", "networkTime"])

# --- 3. Agrupar todos os valores de networkTime em lista por segundo ---
grupos = defaultdict(list)
for _, row in df.iterrows():
    grupos[row["second"]].append(float(row["networkTime"]))

# --- 4. Exibir resultados ---
print("\n=== NetworkTime agrupado por segundo ===")
for segundo in sorted(grupos.keys()):
    valores = grupos[segundo]
    media = sum(valores) / len(valores)
    print(f"{segundo}: {valores}")
    print(f"   ↳ count={len(valores)}, mean={media:.3f} ms\n")

