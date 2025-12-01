import pandas as pd
import re
from collections import Counter

# --- LER DATASET DA APLICAÇÃO ---
df = pd.read_csv("offloading (3).csv")

# Extrai HH:MM:SS do campo textual de timestamp
def extract_second(ts):
    if not isinstance(ts, str):
        return None
    m = re.search(r"(\d{2}:\d{2}:\d{2})", ts)
    return m.group(1) if m else None

df["second"] = df["time"].apply(extract_second)
df = df.dropna(subset=["second", "networkTime"])

# Agrupa todos os networkTime e calcula estatísticas por segundo
df_net = df.groupby("second")["networkTime"].agg(list).reset_index()
df_net["mean_network"] = df_net["networkTime"].apply(lambda x: sum(x)/len(x))

# --- LER LOG DE RETRANSMISSÕES ---
with open("outretrans0.txt", "r", encoding="utf-8", errors="ignore") as f:
    log = f.readlines()

# Extrai segundos do início da linha do log
seg_times = [re.match(r"(\d{2}:\d{2}:\d{2})", linha.strip()).group(1)
             for linha in log if re.match(r"(\d{2}:\d{2}:\d{2})", linha.strip())]

# Conta retransmissões por segundo
contagem = Counter(seg_times)
df_rt = pd.DataFrame(contagem.items(), columns=["second", "retrans_count"])

# --- FAZER O JOIN DAS SÉRIES POR SEGUNDO ---
df_join = pd.merge(df_net, df_rt, on="second", how="left")
df_join["retrans_count"] = df_join["retrans_count"].fillna(0)

# --- RELATÓRIO SIMPLES NA TELA ---
print("\n=== Resumo por Segundo ===")
for _, row in df_join.sort_values("second").iterrows():
    print(f"{row['second']}: {row['mean_network']:.3f} ms "
          f"| retrans={int(row['retrans_count'])}")

# Retorna o DataFrame final se quiser usar depois
df_join

