import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_congestion_window_plot_color_optimized(file_path):
    """
    Gera e salva um gráfico colorido e otimizado da Janela de Congestionamento
    com linhas mais finas e distintos estilos de linha.

    :param file_path: O caminho para o arquivo CSV de entrada.
    """
    try:
        # 1. Carregar os dados
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return
    except pd.errors.EmptyDataError:
        print(f"Erro: O arquivo '{file_path}' está vazio.")
        return
    except KeyError as e:
        print(f"Erro: Coluna não encontrada: {e}. Verifique o cabeçalho.")
        print("Esperado: event,sock,time_us,snd_cwnd,snd_ssthresh,sk_sndbuf,sk_wmem_queued")
        return

    # 2. Preparação de Dados
    time_s = (df['time_us'] - df['time_us'].min()) / 1e6
    df['snd_ssthresh_plot'] = df['snd_ssthresh'].replace(2147483647, np.nan)
    
    # --- Configuração da Espessura da Linha (Diminuída) ---
    LINE_WIDTH = 1.5
    
    # 3. Plotagem com Eixos Duplos Otimizados
    fig, ax1 = plt.subplots(figsize=(16, 8))

    # --- Eixo Y Primário (ax1 - Esquerda): snd_cwnd e snd_ssthresh ---
    
    # snd_cwnd (Janela de Congestionamento)
    ax1.plot(time_s, df['snd_cwnd'], 
             label='snd_cwnd', color='blue', # Cor: Azul
             linewidth=LINE_WIDTH, linestyle='-') # Forma: Sólida

    # snd_ssthresh (Threshold)
    ax1.step(time_s, df['snd_ssthresh_plot'], 
             label='snd_ssthresh', color='red', # Cor: Vermelho
             linewidth=LINE_WIDTH, linestyle='--', where='post') # Forma: Tracejada
    
    # Ajuste de Limites do Eixo Y1 (Mantido da otimização anterior)
    max_cwnd_ssthresh = max(df['snd_cwnd'].max(), df['snd_ssthresh_plot'].max(skipna=True))
    if pd.notna(max_cwnd_ssthresh):
        ax1.set_ylim(bottom=0, top=max_cwnd_ssthresh * 1.1)
    else: 
        ax1.set_ylim(bottom=0, top=df['snd_cwnd'].max() * 1.5)
        
    ax1.set_xlabel('Tempo (ms)', fontsize=14)
    ax1.set_ylabel('snd_cwnd, snd_ssthresh (segmentos/MSS)', color='black', fontsize=14)
    ax1.tick_params(axis='y', labelcolor='black', labelsize=12)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.tick_params(axis='x', labelsize=12)


    # --- Eixo Y Secundário (ax2 - Direita): sk_sndbuf e sk_wmem_queued ---
    ax2 = ax1.twinx()

    # sk_sndbuf (Tamanho do Buffer)
    ax2.step(time_s, df['sk_sndbuf'], 
             label='sk_sndbuf', color='black', # Cor: Verde
             linewidth=LINE_WIDTH, linestyle='-.', alpha=0.999, where='post') # Forma: Traço-Ponto

    # sk_wmem_queued (Dados na Fila)
    ax2.plot(time_s, df['sk_wmem_queued'], 
             label='sk_wmem_queued', color='green', # Cor: Roxo
             linewidth=LINE_WIDTH, linestyle=':', alpha=0.8) # Forma: Pontilhada

    # Ajuste de Limites do Eixo Y2 (Mantido da otimização anterior)
    max_wmem_sndbuf = max(df['sk_wmem_queued'].max(), df['sk_sndbuf'].max())
    min_wmem_sndbuf = min(df['sk_wmem_queued'].min(), df['sk_sndbuf'].min())
    if df['sk_wmem_queued'].max() > 0 and df['sk_wmem_queued'].max() != df['sk_wmem_queued'].min():
        ax2.set_ylim(bottom=max(0, min_wmem_sndbuf * 0.9), top=max_wmem_sndbuf * 1.1)
    else:
        ax2.set_ylim(bottom=0, top=df['sk_sndbuf'].max() * 1.1)

    ax2.set_ylabel('sk_sndbuf, sk_wmem_queued (bytes)', color='black', fontsize=14)
    ax2.tick_params(axis='y', labelcolor='black', labelsize=12)
    ax2.ticklabel_format(style='plain', axis='y')
    
    # 4. Legenda e Título
    plt.title('Análise da Janela de Congestionamento TCP e Status de Buffer - Teste 3%', fontsize=16)
    
    # Combina as legendas de ambos os eixos
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, 
               loc='upper left', fontsize=12, frameon=True, edgecolor='black', fancybox=False)

    # 5. Salvar o Gráfico
    plt.tight_layout()
    plot_filename = 'congestion_window123_plot_colorido.png'
    plt.savefig(plot_filename, dpi=400)
    print(f"Gráfico de análise de congestionamento colorido salvo como: {plot_filename}")

# --- EXEMPLO DE USO ---
# **Importante:** Substitua 'out.csv' pelo nome do seu arquivo real.
generate_congestion_window_plot_color_optimized('out0.csv')
