import pandas as pd
import re

# --- 1. Contar retransmissões totais no log ---
retrans_total = 0
with open("outretrans0.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        # Consideramos qualquer linha que comece com timestamp HH:MM:SS como um evento de retransmissão
        if re.match(r"\d{2}:\d{2}:\d{2}", line.strip()):
            retrans_total += 1

# --- 2. Somar o tempo total de rede no CSV ---
df = pd.read_csv("offloading (3).csv", sep=None, engine="python")
# Tentar encontrar a coluna networkTime (pode vir com nome exato ou pequenas variações)
col_net = None
for c in df.columns:
    if "network" in c.lower():
        col_net = c
        break

if col_net is None:
    print("⚠️ Coluna de networkTime não encontrada no CSV!")
    exit()

network_time_total = df[col_net].dropna().sum()

# --- 3. Relatório ---
print("\n=== Métricas extraídas ===")
print(f"Total de retransmissões TCP: {retrans_total} eventos")
print(f"Tempo total de rede da aplicação: {network_time_total:.3f} ms")
print(f"Tempo total de rede (segundos): {network_time_total/1000:.3f} s")
print("==========================\n")

