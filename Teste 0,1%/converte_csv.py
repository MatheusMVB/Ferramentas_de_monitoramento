import pandas as pd
import re
import sys

# --- 1. Ler CSV ---
try:
    df = pd.read_csv("offloading (3).csv", sep=None, engine="python")
except FileNotFoundError:
    print("❌ Arquivo offloading (3).csv não encontrado!", file=sys.stderr)
    sys.exit(1)

# --- 2. Extrair horário HH:MM:SS da coluna time (se existir), mantendo vazios ---
if "time" in df.columns:
    def extrai_hora(x):
        if not isinstance(x, str):
            return ""
        m = re.search(r"\d{2}:\d{2}:\d{2}", x)
        return m.group(0) if m else ""

    df["time"] = df["time"].apply(extrai_hora)

# --- 3. Limitar floats para 2 casas decimais ---
for c in df.select_dtypes(include=["float"]).columns:
    df[c] = df[c].round(2)

# --- 4. Imprimir TSV ---
print("\t".join(df.columns))
for _, row in df.iterrows():
    print("\t".join("" if pd.isna(x) or str(x) == "nan" else str(x) for x in row))

