import re
import matplotlib.pyplot as plt
import sys

def parse_tests(text):
    tests = []
    current = {}
    for line in text.splitlines():
        line = line.strip()
        m_label = re.match(r"^Teste\s+([\d\.]+)\%?$", line, re.I)
        if m_label:
            if current:
                tests.append(current)
            current = {"label": f"Teste {m_label.group(1)}%", "retrans": None, "netms": None}
            continue
        m_retrans = re.search(r"Total de retransmissões TCP:\s*(\d+)", line, re.I)
        if m_retrans:
            current["retrans"] = int(m_retrans.group(1))
            continue
        m_netms = re.search(r"Tempo total de rede.*?:\s*([\d\.]+)\s*ms", line, re.I)
        if m_netms:
            current["netms"] = float(m_netms.group(1))
            continue
    if current:
        tests.append(current)
    return [t for t in tests if t["retrans"] is not None and t["netms"] is not None]

print("Lendo resultados...", file=sys.stderr)

with open("resultados.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

tests = parse_tests(text)
if not tests:
    print("⚠️ Nenhum teste válido!")
    sys.exit(1)

labels = [t["label"] for t in tests]
retrans = [t["retrans"] for t in tests]
netms = [t["netms"] for t in tests]

x = range(len(labels))
width = 0.35

# ===== GRÁFICO 1: BARRAS (mantido) =====
fig, ax1 = plt.subplots()

ax1.bar([p - width/2 for p in x], retrans, width, label="Retransmissões", color="tab:blue")
ax1.set_ylabel("Retransmissões")

ax2 = ax1.twinx()
ax2.bar([p + width/2 for p in x], netms, width, label="Tempo de Rede (ms)", color="tab:red")
ax2.set_ylabel("Tempo de Rede (ms)")

handles1, _ = ax1.get_legend_handles_labels()
handles2, _ = ax2.get_legend_handles_labels()
ax1.legend(handles=handles1 + handles2)

ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=30)
ax1.set_title("Retransmissões × Tempo de Rede (ms)")

plt.tight_layout()
plt.show()

# ===== GRÁFICO 2: LINHAS (novo, estilo semelhante) =====
plt.rcParams.update({
    "figure.figsize": (12, 6.5),
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})

fig2, ax = plt.subplots()
ax.plot(labels, retrans, marker="o", label="Retransmissões", color='blue')
ax.plot(labels, netms, marker="s", label="Tempo de Rede (ms)", color='red')

ax.set_ylabel("Valores")
ax.set_title("Retransmissões × Tempo de Rede (ms)")

# Legenda combinada centralizada acima (como o último gráfico que você gostou)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.12),
    ncol=2,
    frameon=True
)

plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# ===== Resumo no console =====
print("\nResumo dos testes:")
for lb, r, nm in zip(labels, retrans, netms):
    print(f"{lb}: retrans={r} | netms={nm} ms")

