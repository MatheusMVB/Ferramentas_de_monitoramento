import re
import sys
import matplotlib.pyplot as plt

def parse_tests(text):
    tests = []
    current = None

    for line in text.splitlines():
        line = line.strip()

        # Detecta início do teste
        m_label = re.match(r"^Teste\s+([\d\.]+)\%?$", line, re.I)
        if m_label:
            if current:
                tests.append(current)
            current = {
                "label": f"Teste {m_label.group(1)}%",
                "frames": None,
                "retrans": None,
                "rpf": None,
                "netms": None,
            }
            continue

        if current is None:
            continue

        # Capturas
        if (m := re.search(r"Total de Frames Processados:\s*(\d+)", line, re.I)):
            current["frames"] = int(m.group(1))
        if (m := re.search(r"Total de Retransmissões TCP:\s*(\d+)", line, re.I)):
            current["retrans"] = int(m.group(1))
        if (m := re.search(r"Retransmissões por Frame.*?:\s*([\d\.]+)", line, re.I)):
            current["rpf"] = float(m.group(1))
        if (m := re.search(r"Tempo total de rede.*?:\s*([\d\.]+)\s*ms", line, re.I)):
            current["netms"] = float(m.group(1))

    if current:
        tests.append(current)

    # Mantém só os completos
    return [t for t in tests if None not in (t["frames"], t["retrans"], t["rpf"], t["netms"])]

# --- Leitura do arquivo ---
with open("resultados.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

tests = parse_tests(text)
if not tests:
    print("⚠️ Nenhum teste válido encontrado!", file=sys.stderr)
    sys.exit(1)

labels = [t["label"] for t in tests]
frames = [t["frames"] for t in tests]
retrans = [t["retrans"] for t in tests]
rpf = [t["rpf"] for t in tests]
netms = [t["netms"] for t in tests]

x = list(range(len(labels)))
w = 0.35

# Aumenta fontes do eixo e altura da figura
plt.rcParams.update({
    "figure.figsize": (12, 6.5),
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
})

# ========== GRÁFICO 1: Frames e Retrans/Frame ==========
fig1, ax1 = plt.subplots()

b1 = ax1.bar([p - w/2 for p in x], frames, w, color="tab:green")
ax1.set_ylabel("Frames Processados")

ax1_twin = ax1.twinx()
b2 = ax1_twin.bar([p + w/2 for p in x], rpf, w, color="tab:purple")
ax1_twin.set_ylabel("Retransmissões por Frame")

ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=25)
ax1.set_title("Frames × Retransmissões por Frame")

# Legenda interna em área segura (topo central, sem barras)
ax1.legend(
    handles=[b1, b2],
    labels=["Frames Processados", "Retrans por Frame (média)"],
    loc="upper center",
    bbox_to_anchor=(0.5, 1.12),  # sobe a legenda um pouco acima do topo do eixo
    ncol=2,
    frameon=True
)

plt.tight_layout()
plt.show()

# ========== GRÁFICO 2: Tempo de Rede (ms) e Retrans Total ==========
fig2, ax2 = plt.subplots()

b3 = ax2.bar([p - w/2 for p in x], retrans, w, color="tab:blue")
ax2.set_ylabel("Retransmissões Totais")

ax2_twin = ax2.twinx()
b4 = ax2_twin.bar([p + w/2 for p in x], netms, w, color="tab:red")
ax2_twin.set_ylabel("Tempo de Rede Total (ms)")

ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=25)
ax2.set_title("Tempo de Rede (ms) × Retransmissões Totais")

# Legenda interna, também em área segura
ax2.legend(
    handles=[b3, b4],
    labels=["Retrans TCP Total", "Tempo de Rede Total (ms)"],
    loc="upper center",
    bbox_to_anchor=(0.5, 1.12),
    ncol=2,
    frameon=True
)

plt.tight_layout()
plt.show()

# ========== Resumo no console ==========
print("\n=== Métricas extraídas ===")
print(f"Total de Frames: {sum(frames)} frames")
print(f"Total de Retransmissões: {sum(retrans)} eventos")
print(f"Retransmissões/Frame global (média): {sum(retrans)/sum(frames):.2f} retrans/frame")
print(f"Tempo de Rede Total: {sum(netms):.2f} ms")
print("=========================\n")

