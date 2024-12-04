import tkinter as tk
from tkinter import ttk
import random

# Função para simular a lógica do Sequenciador Móvel com agrupamento de mensagens por cliente
def sequenciamento_movel(clientes, sequenciadores, receptores, mensagens_por_cliente):
    tabela_emissor = []
    tabela_sequenciador = []
    tabela_receptor = []
    mensagens_recebidas = []
    ordem_aleatoria = {}
    token_idx = 0  # Índice do sequenciador com o token
    ordem_atual = 1  # Ordem inicial para mensagens

    # Gerar ordens aleatórias para cada cliente
    for cliente in clientes:
        quantidade_mensagens = mensagens_por_cliente
        ordem_cliente = list(range(ordem_atual, ordem_atual + quantidade_mensagens))
        random.shuffle(ordem_cliente)  # Permutação aleatória da ordem
        ordem_aleatoria[cliente] = ordem_cliente
        ordem_atual += quantidade_mensagens

    # Gerar as mensagens para cada cliente
    mensagem_id = 1
    for cliente in clientes:
        sequenciador_com_token = sequenciadores[token_idx]  # Sequenciador responsável por este cliente
        for idx, ordem in enumerate(ordem_aleatoria[cliente]):
            mensagem = f"M{mensagem_id}"
            mensagens_recebidas.append((mensagem, ordem))  # Vincular mensagem à sua ordem

            # Preencher a tabela do emissor
            tabela_emissor.append({
                "Cliente": cliente,
                "Mensagem Enviada": mensagem,
                "Mensagens Restantes": mensagens_por_cliente * len(clientes) - mensagem_id
            })

            # Preencher a tabela do sequenciador
            tabela_sequenciador.append({
                "Sequenciador": ",".join(sequenciadores),
                "Sequenciador com Token": sequenciador_com_token,
                "Mensagem Processada": mensagem,
                "Token Atual": "Sim" if sequenciador_com_token else "Não",
                "Mensagens Processadas": mensagem_id,
                "Ordem Aleatória": ordem
            })

            # Avançar para a próxima mensagem
            mensagem_id += 1

        # Passar o token para o próximo sequenciador
        token_idx = (token_idx + 1) % len(sequenciadores)

    # Ordenar mensagens recebidas na tabela receptor com base na ordem aleatória
    mensagens_recebidas.sort(key=lambda x: x[1])  # Ordenar pela ordem aleatória

    # Criar a tabela receptor incremental
    for i in range(1, len(mensagens_recebidas) + 1):
        tabela_receptor.append({
            "Receptores": ",".join(receptores),
            "Mensagens Recebidas": ", ".join([mensagem for mensagem, _ in mensagens_recebidas[:i]])
        })

    return tabela_emissor, tabela_sequenciador, tabela_receptor

# Função para criar e exibir uma tabela no Tkinter
def criar_tabela(frame, titulo, colunas):
    # Criar a Treeview para exibir os dados
    tree = ttk.Treeview(frame, columns=colunas, show='headings')
    tree.pack(expand=True, fill=tk.BOTH)

    # Configurar os cabeçalhos das colunas
    for coluna in colunas:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, width=150, anchor="center")

    return tree

# Função para preencher as tabelas em tempo real
def preencher_tabelas(janela, tabelas, dados, intervalo, indice=0):
    if indice < len(dados[0]):  # Enquanto houver dados para preencher
        for tabela, data in zip(tabelas, dados):
            tabela.insert("", tk.END, values=list(data[indice].values()))
        janela.after(intervalo, preencher_tabelas, janela, tabelas, dados, intervalo, indice + 1)

# Função principal para criar as tabelas e iniciar o preenchimento
def criar_tabelas_principais(tabela_emissor, tabela_sequenciador, tabela_receptor):
    # Configuração da janela principal
    janela = tk.Tk()
    janela.title("Sequenciador Móvel - Tabelas Dinâmicas")

    # Criar frames para cada tabela
    frame_emissor = tk.LabelFrame(janela, text="Tabela do Emissor")
    frame_emissor.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    frame_sequenciador = tk.LabelFrame(janela, text="Tabela do Sequenciador")
    frame_sequenciador.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    frame_receptor = tk.LabelFrame(janela, text="Tabela do Receptor")
    frame_receptor.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    # Criar as tabelas
    colunas_emissor = list(tabela_emissor[0].keys())
    tabela_emissor_tree = criar_tabela(frame_emissor, "Tabela do Emissor", colunas_emissor)

    colunas_sequenciador = list(tabela_sequenciador[0].keys())
    tabela_sequenciador_tree = criar_tabela(frame_sequenciador, "Tabela do Sequenciador", colunas_sequenciador)

    colunas_receptor = list(tabela_receptor[0].keys())
    tabela_receptor_tree = criar_tabela(frame_receptor, "Tabela do Receptor", colunas_receptor)

    # Iniciar preenchimento gradual das tabelas
    preencher_tabelas(
        janela,
        [tabela_emissor_tree, tabela_sequenciador_tree, tabela_receptor_tree],
        [tabela_emissor, tabela_sequenciador, tabela_receptor],
        intervalo=5000  # Intervalo de 2 segundos entre cada atualização
    )

    # Botão para fechar a aplicação
    tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)

    # Rodar a aplicação Tkinter
    janela.mainloop()

# Configurações do sistema
clientes = ["C1", "C2", "C3"]
sequenciadores = ["S1", "S2", "S3"]
receptores = ["R1", "R2", "R3"]
mensagens_por_cliente = 2

# Simular o sistema
tabela_emissor, tabela_sequenciador, tabela_receptor = sequenciamento_movel(clientes, sequenciadores, receptores, mensagens_por_cliente)

# Exibir os resultados em tabelas separadas no Tkinter
criar_tabelas_principais(tabela_emissor, tabela_sequenciador, tabela_receptor)