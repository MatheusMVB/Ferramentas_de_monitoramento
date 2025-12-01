import re
import matplotlib.pyplot as plt

# --- 1. Ler e extrair métricas por teste ---
testes = []
iseg_totals = []
oseg_totals = []

bloco_teste = None
total_iseg = None
total_oseg = None

with open("resultadosar.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()

        # Detecta início de um novo teste
        m_teste = re.match(r"Teste\s+([\d\.]+%)", line, re.IGNORECASE)
        if m_teste:
            if bloco_teste and total_iseg is not None and total_oseg is not None:
                testes.append(bloco_teste)
                iseg_totals.append(total_iseg)
                oseg_totals.append(total_oseg)

            bloco_teste = m_teste.group(1)
            total_iseg = None
            total_oseg = None
            continue

        # Extrai total RECEBIDO
        m_iseg = re.match(r"Total de segmentos RECEBIDOS.*?:\s+(\d+)", line)
        if m_iseg:
            total_iseg = int(m_iseg.group(1))

        # Extrai total ENVIADO
        m_oseg = re.match(r"Total de segmentos ENVIADOS.*?:\s+(\d+)", line)
        if m_oseg:
            total_oseg = int(m_oseg.group(1))

    # Salva o último teste
    if bloco_teste and total_iseg is not None and total_oseg is not None:
        testes.append(bloco_teste)
        iseg_totals.append(total_iseg)
        oseg_totals.append(total_oseg)

# --- 2. Configurações de gráfico estilo "retrans × tempo" ---
x = range(len(testes))
width = 0.35

plt.rcParams.update({
    "figure.figsize": (12, 6.5),
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})

fig, ax1 = plt.subplots()

# Barras de segmentos RECEBIDOS
ax1.bar([p - width/2 for p in x], iseg_totals, width, label="Segmentos RECEBIDOS", color="tab:blue")
ax1.set_ylabel("Segmentos RECEBIDOS")

# Segundo eixo para segmentos ENVIADOS
ax2 = ax1.twinx()
ax2.bar([p + width/2 for p in x], oseg_totals, width, label="Segmentos ENVIADOS", color="tab:red")
ax2.set_ylabel("Segmentos ENVIADOS")

# Legenda combinada
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
ax1.set_xticklabels(testes, rotation=30)
ax1.set_title("Segmentos TCP Enviados × Recebidos por Teste")

plt.tight_layout()
plt.show()

