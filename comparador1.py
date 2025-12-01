import pandas as pd
import re
from datetime import datetime
from scipy.stats import pearsonr

# --- 1. Ler CSV da aplicação ---
df = pd.read_csv("offloading (3).csv")

# Extrair segundos HH:MM:SS do campo de timestamp textual
def extract_second(ts):
    if not isinstance(ts, str):
        return None
    m = re.search(r"(\d{2}:\d{2}:\d{2})", ts)
    return m.group(1) if m else None

df["second"] = df["time"].apply(extract_second)
df = df.dropna(subset=["second"])

# Converter timestamp completo para datetime (campo extra, caso precise no futuro)
def parse_full_ts(ts):
    try:
        full = re.search(r"(\w{3} \w{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})", ts)
        if not full:
            return None
        return datetime.strptime(full.group(1), "%a %b %d %Y %H:%M:%S")
    except:
        return None

df["ts"] = df["time"].apply(parse_full_ts)
df = df.dropna(subset=["ts"])

# Agregar networkTime médio por segundo
df_app = df.groupby("second")["networkTime"].mean().reset_index()

# --- 2. Ler retransmissões ---
retrans_times = []
with open("outretrans0.txt", "r") as f:
    for line in f:
        m = re.match(r"(\d{2}:\d{2}:\d{2})", line.strip())
        if m:
            retrans_times.append(m.group(1))

# Contar retransmissões por segundo
df_rt = pd.DataFrame(retrans_times, columns=["second"])
df_rt = df_rt.groupby("second").size().reset_index(name="retrans_count")

# --- 3. Unir datasets ---
df_join = pd.merge(df_app, df_rt, on="second", how="left")
df_join["retrans_count"] = df_join["retrans_count"].fillna(0)

if df_join.empty:
    print("\n⚠️ Nenhuma interseção temporal entre os arquivos.")
    exit()

# --- 4. Calcular Correlação de Pearson ---
if df_join["retrans_count"].sum() > 1:
    r, p = pearsonr(df_join["networkTime"], df_join["retrans_count"])
else:
    r, p = 0, 1

# --- 5. Calcular networkTime médio em momentos COM e SEM retransmissão ---
no_retrans = df_join[df_join["retrans_count"] == 0]["networkTime"]
with_retrans = df_join[df_join["retrans_count"] > 0]["networkTime"]

baseline = no_retrans.mean() if not no_retrans.empty else None
high_net = with_retrans.mean() if not with_retrans.empty else None
increase = high_net - baseline if (baseline is not None and high_net is not None) else None

# --- 6. Relatório ---
print("\n=== Resultado da Análise ===")
if baseline is not None:
    print(f"Média networkTime sem retransmissão: {baseline:.3f} ms")
else:
    print("⚠️ Sem amostras suficientes sem retransmissão")

if high_net is not None:
    print(f"Média networkTime com retransmissão: {high_net:.3f} ms")
    if increase is not None:
        print(f"Aumento médio estimado: {increase:.3f} ms")
else:
    print("⚠️ Não há segundos com retransmissões no join")

print(f"\nCorrelação de Pearson: r={r:.4f}, p={p:.4f}")

if increase and increase > 5:
    print("📈 O tempo de rede aumenta quando há retransmissões.")
else:
    print("📉 Não foi detectado aumento expressivo do tempo de rede ligado às retransmissões.")

if r > 0.5:
    print("✅ Correlação forte: retransmissões estão associadas ao aumento do tempo de rede.")
elif r > 0.3:
    print("⚠️ Correlação moderada: pode haver influência parcial.")
else:
    print("❌ Correlação fraca: retransmissões não explicam sozinhas o aumento.")

print("\nTop 10 segundos com mais retransmissões:")
print(df_join.sort_values("retrans_count", ascending=False).head(10))

