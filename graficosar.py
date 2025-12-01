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
            # Se já estávamos coletando um teste anterior, salva antes de iniciar outro
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

    # Após o loop, salva o último bloco encontrado
    if bloco_teste and total_iseg is not None and total_oseg is not None:
        testes.append(bloco_teste)
        iseg_totals.append(total_iseg)
        oseg_totals.append(total_oseg)

# --- 2. Gerar o gráfico de barras ---
x = range(len(testes))
largura = 0.35

plt.figure(figsize=(10, 6))

plt.bar([i - largura/2 for i in x], iseg_totals, width=largura, label="Segmentos RECEBIDOS (iseg)")
plt.bar([i + largura/2 for i in x], oseg_totals, width=largura, label="Segmentos ENVIADOS (oseg)")

plt.xticks(x, testes)
plt.ylabel("Quantidade total de segmentos")
plt.title("Comparação de Segmentos TCP Enviados e Recebidos por Teste")

# Ajusta a posição da legenda para não cobrir as barras
plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=True)

plt.tight_layout()
plt.show()

# --- 3. Caso queira ver no console também ---
print("\nResumo extraído para o gráfico:")
for t, i, o in zip(testes, iseg_totals, oseg_totals):
    print(f"{t}: iseg={i} | oseg={o}")

