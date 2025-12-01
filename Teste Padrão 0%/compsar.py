import re

time_pattern = r"(\d{2}:\d{2}:\d{2})"

active_times = []
total_iseg = 0
total_oseg = 0

with open("outsar0.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()

        # Captura o timestamp no início da linha
        m = re.match(rf"{time_pattern}\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)", line)
        if not m:
            continue

        ts, active_s, passive_s, iseg_s, oseg_s = m.groups()

        # Converter valores que usam vírgula para float
        iseg = float(iseg_s.replace(",", ""))
        oseg = float(oseg_s.replace(",", ""))

        # Ignora segundos sem envio/recepção (conexão inativa)
        if iseg == 0 and oseg == 0:
            continue

        active_times.append(ts)
        total_iseg += iseg
        total_oseg += oseg

print("\n=== Análise de Segmentos TCP ===")
print(f"Segundos com conexão ativa: {len(active_times)} segundos")
print(f"Total de segmentos RECEBIDOS (iseg): {int(total_iseg)} segmentos")
print(f"Total de segmentos ENVIADOS   (oseg): {int(total_oseg)} segmentos")
print(f"Total agregado (enviados + recebidos): {int(total_iseg + total_oseg)} segmentos")

print("\nMomentos onde houve tráfego TCP:")
for t in active_times:
    print("→", t)

print("===============================\n")

