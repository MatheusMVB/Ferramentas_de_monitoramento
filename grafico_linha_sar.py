import re
import matplotlib.pyplot as plt
import sys

def parse_testes(text):
    tests = []
    current = {}
    for line in text.splitlines():
        line = line.strip()

        # Detecta início de novo teste
        m_label = re.match(r"^Teste\s+([\d\.]+%)", line, re.IGNORECASE)
        if m_label:
            if current.get("iseg") is not None and current.get("oseg") is not None:
                tests.append(current)
            current = {"label": m_label.group(1), "iseg": None, "oseg": None}
            continue

        # Extrai total de segmentos RECEBIDOS
        m_iseg = re.search(r"Total de segmentos RECEBIDOS.*?:\s*(\d+)", line, re.I)
        if m_iseg:
            current["iseg"] = int(m_iseg.group(1))
            continue

        # Extrai total de segmentos ENVIADOS
        m_oseg = re.search(r"Total de segmentos ENVIADOS.*?:\s*(\d+)", line, re.I)
        if m_oseg:
            current["oseg"] = int(m_oseg.group(1))
            continue

    # Salva o último teste válido
    if current.get("iseg") is not None and current.get("oseg") is not None:
        tests.append(current)

    return tests

print("Lendo resultados...", file=sys.stderr)

with open("resultadosar.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

tests = parse_testes(text)
if not tests:
    print("⚠️ Nenhum teste válido encontrado!")
    sys.exit(1)

labels = [t["label"] for t in tests]
iseg = [t["iseg"] for t in tests]
oseg = [t["oseg"] for t in tests]

# Configura tamanho do gráfico e fontes (sem definir cores específicas)
plt.rcParams.update({
    "figure.figsize": (12, 6.5),
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})

fig, ax = plt.subplots()

# Plot linhas
ax.plot(labels, iseg, marker="o", label="Segmentos RECEBIDOS")
ax.plot(labels, oseg, marker="s", label="Segmentos ENVIADOS")

ax.set_ylabel("Quantidade de Segmentos")
ax.set_title("Segmentos TCP Enviados × Recebidos por Teste")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=2, frameon=True)

plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# Resumo no console
print("\nResumo extraído:")
for t, i, o in zip(labels, iseg, oseg):
    print(f"{t}: RECEBIDOS={i} | ENVIADOS={o}")

