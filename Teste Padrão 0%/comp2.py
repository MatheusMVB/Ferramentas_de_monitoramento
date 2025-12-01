import pandas as pd
import re
import sys

# --- 1. Contar retransmissões totais no log ---
retrans_total = 0
with open("outretrans0.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if re.match(r"\d{2}:\d{2}:\d{2}", line.strip()):
            retrans_total += 1

# --- 2. Ler o CSV e calcular tempo total de rede ---
df = pd.read_csv("offloading (3).csv", sep=None, engine="python")

# Captura a coluna de networkTime (verifica variações no nome)
col_net = next((c for c in df.columns if "network" in c.lower()), None)
if col_net is None:
    print("⚠️ Coluna de networkTime não encontrada no CSV!", file=sys.stderr)
    sys.exit(1)

network_time_total = df[col_net].dropna().sum()

# --- 3. Calcular total de frames e retransmissões por frame ---
frames_total = len(df)
retrans_per_frame_avg = retrans_total / frames_total if frames_total > 0 else float("nan")

# --- 4. Relatório final ---
print("\n=== Métricas extraídas ===")
print(f"Total de Frames Processados: {frames_total} frames")
print(f"Total de Retransmissões TCP: {retrans_total} eventos")
print(f"Retransmissões por Frame (média): {retrans_per_frame_avg:.3f} retrans/frame")
print(f"Tempo total de rede da aplicação: {network_time_total:.3f} ms")
print(f"Tempo total de rede (segundos): {network_time_total/1000:.3f} s")
print("==========================\n")

