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

# Aumenta fontes e tamanho da figura (mais alta)
plt.rcParams.update({
    "figure.figsize": (12, 6.5),
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})

fig, ax1 = plt.subplots()

# Barra de retransmissões (cor original mantida)
ax1.bar([p - width/2 for p in x], retrans, width, label="Retransmissões", color="tab:blue")
ax1.set_ylabel("Retransmissões")

# Segunda escala para tempo (em ms) (cor original mantida)
ax2 = ax1.twinx()
ax2.bar([p + width/2 for p in x], netms, width, label="Tempo de Rede (ms)", color="tab:red")
ax2.set_ylabel("Tempo de Rede (ms)")

# Legenda combinada dentro da figura, deslocada para área segura
handles1, _ = ax1.get_legend_handles_labels()
handles2, _ = ax2.get_legend_handles_labels()
ax1.legend(
    handles=handles1 + handles2,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.15),
    ncol=2,
    frameon=True
)

ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=30)
ax1.set_title("Retransmissões × Tempo de Rede (ms)")

plt.tight_layout()
plt.show()

