from collections import Counter
import re
import pandas as pd

arquivo = "outretrans0.txt"

segundos = []
with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
    for linha in f:
        # Extrai padrão HH:MM:SS no início da linha
        m = re.match(r"(\d{2}:\d{2}:\d{2})", linha.strip())
        if m:
            segundos.append(m.group(1))

# Conta retransmissões por segundo
contador = Counter(segundos)

# Converte para um DataFrame e exibe ordenado pelo tempo
df = pd.DataFrame(contador.items(), columns=["segundo", "retransmissoes"])
df = df.sort_values("segundo")

print("\n=== Retransmissões por Segundo ===")
print(df.to_string(index=False))

