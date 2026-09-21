import tkinter as tk
from tkinter import messagebox


# ============================================================
# MAPA DA CIDADE
# ============================================================

INICIO = "Base de Atendimento"
OBJETIVO = "Hospital Central"

# Cada estado possui uma lista com seus vizinhos.
GRAFO = {
    "Base de Atendimento": ["Centro", "Parque Municipal", "Rodoviária"],
    "Centro": ["Base de Atendimento", "Shopping", "Universidade", "Praça Central"],
    "Parque Municipal": ["Base de Atendimento", "Universidade", "Terminal Norte"],
    "Rodoviária": ["Base de Atendimento", "Terminal Norte", "Aeroporto"],
    "Shopping": ["Centro", "Praça Central", "Universidade"],
    "Universidade": ["Centro", "Parque Municipal", "Shopping", "Ponte Central", "Beco Histórico"],
    "Terminal Norte": ["Parque Municipal", "Rodoviária", "Ponte Central", "Aeroporto"],
    "Praça Central": ["Centro", "Shopping", "Ponte Central"],
    "Beco Histórico": ["Universidade"],
    "Ponte Central": ["Universidade", "Terminal Norte", "Aeroporto", "Praça Central", "Hospital Central"],
    "Aeroporto": ["Rodoviária", "Terminal Norte", "Ponte Central"],
    "Hospital Central": ["Ponte Central"]
}


# h(n) representa uma estimativa da distância até o Hospital Central.
HEURISTICA_ORIGINAL = {
    "Base de Atendimento": 14,
    "Centro": 10,
    "Parque Municipal": 7,
    "Rodoviária": 12,
    "Shopping": 6,
    "Universidade": 5,
    "Terminal Norte": 8,
    "Praça Central": 4,
    "Beco Histórico": 2,
    "Ponte Central": 3,
    "Aeroporto": 6,
    "Hospital Central": 0
}


# Segunda execução: somente alguns valores foram alterados.
HEURISTICA_MODIFICADA = {
    "Base de Atendimento": 14,
    "Centro": 4,
    "Parque Municipal": 13,
    "Rodoviária": 12,
    "Shopping": 6,
    "Universidade": 11,
    "Terminal Norte": 8,
    "Praça Central": 4,
    "Beco Histórico": 2,
    "Ponte Central": 3,
    "Aeroporto": 6,
    "Hospital Central": 0
}


# Posições usadas apenas para desenhar o mapa.
POSICOES = {
    "Base de Atendimento": (90, 330),
    "Centro": (240, 150),
    "Parque Municipal": (240, 330),
    "Rodoviária": (225, 520),
    "Shopping": (415, 95),
    "Universidade": (420, 275),
    "Terminal Norte": (410, 475),
    "Praça Central": (575, 145),
    "Beco Histórico": (625, 255),
    "Ponte Central": (600, 385),
    "Aeroporto": (575, 535),
    "Hospital Central": (765, 330)
}


# Lista das conexões usada somente para desenhar as linhas do mapa.
CONEXOES = [
    ("Base de Atendimento", "Centro"),
    ("Base de Atendimento", "Parque Municipal"),
    ("Base de Atendimento", "Rodoviária"),
    ("Centro", "Shopping"),
    ("Centro", "Universidade"),
    ("Centro", "Praça Central"),
    ("Parque Municipal", "Universidade"),
    ("Parque Municipal", "Terminal Norte"),
    ("Rodoviária", "Terminal Norte"),
    ("Rodoviária", "Aeroporto"),
    ("Shopping", "Praça Central"),
    ("Shopping", "Universidade"),
    ("Universidade", "Ponte Central"),
    ("Universidade", "Beco Histórico"),
    ("Terminal Norte", "Ponte Central"),
    ("Terminal Norte", "Aeroporto"),
    ("Aeroporto", "Ponte Central"),
    ("Praça Central", "Ponte Central"),
    ("Ponte Central", "Hospital Central")
]


class BuscaHeuristicaVisual:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Busca Heurística - Rota de Emergência")

        # Escolhe qual heurística será usada.
        self.tipo_heuristica = tk.StringVar(value="original")

        self.canvas = tk.Canvas(
            janela,
            width=850,
            height=620,
            bg="white"
        )
        self.canvas.grid(row=0, column=0, rowspan=15, padx=20, pady=20)

        tk.Label(
            janela,
            text="Busca Heurística",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=1, sticky="w")

        tk.Label(
            janela,
            text="Desempate: ordem alfabética",
            font=("Arial", 10)
        ).grid(row=1, column=1, sticky="w")

        frame_modo = tk.Frame(janela)
        frame_modo.grid(row=2, column=1, sticky="w", pady=5)

        tk.Radiobutton(
            frame_modo,
            text="Original",
            variable=self.tipo_heuristica,
            value="original",
            command=self.reiniciar
        ).pack(side="left")

        tk.Radiobutton(
            frame_modo,
            text="Modificada",
            variable=self.tipo_heuristica,
            value="modificada",
            command=self.reiniciar
        ).pack(side="left")

        self.lbl_passo = tk.Label(janela, text="Passo: 0", font=("Arial", 11, "bold"))
        self.lbl_passo.grid(row=3, column=1, sticky="w")

        self.lbl_atual = tk.Label(janela, text="Estado atual: -", font=("Arial", 11))
        self.lbl_atual.grid(row=4, column=1, sticky="w")

        self.lbl_novos = tk.Label(janela, text="Novos estados: -", font=("Arial", 11))
        self.lbl_novos.grid(row=5, column=1, sticky="w")

        self.lbl_proximo = tk.Label(janela, text="Próximo: Base de Atendimento", font=("Arial", 11))
        self.lbl_proximo.grid(row=6, column=1, sticky="w")

        tk.Label(
            janela,
            text="Estados disponíveis:",
            font=("Arial", 11, "bold")
        ).grid(row=7, column=1, sticky="w", pady=(10, 0))

        self.txt_disponiveis = tk.Text(janela, width=43, height=6, font=("Courier", 10))
        self.txt_disponiveis.grid(row=8, column=1, sticky="w")

        tk.Label(
            janela,
            text="Explicação:",
            font=("Arial", 11, "bold")
        ).grid(row=9, column=1, sticky="w", pady=(10, 0))

        self.lbl_explicacao = tk.Label(
            janela,
            text="Clique em 'Próximo passo' para iniciar.",
            justify="left",
            wraplength=390,
            font=("Arial", 10)
        )
        self.lbl_explicacao.grid(row=10, column=1, sticky="w")

        frame_botoes = tk.Frame(janela)
        frame_botoes.grid(row=11, column=1, pady=10, sticky="w")

        tk.Button(
            frame_botoes,
            text="Próximo passo",
            command=self.proximo_passo,
            width=14
        ).pack(side="left", padx=3)

        tk.Button(
            frame_botoes,
            text="Executar tudo",
            command=self.executar_tudo,
            width=12
        ).pack(side="left", padx=3)

        tk.Button(
            frame_botoes,
            text="Reiniciar",
            command=self.reiniciar,
            width=10
        ).pack(side="left", padx=3)

        tk.Label(
            janela,
            text="Resultado:",
            font=("Arial", 11, "bold")
        ).grid(row=12, column=1, sticky="w")

        self.txt_resultado = tk.Text(janela, width=43, height=11, font=("Courier", 9))
        self.txt_resultado.grid(row=13, column=1, sticky="w")

        self.reiniciar()

    def pegar_heuristica(self):
        if self.tipo_heuristica.get() == "modificada":
            return HEURISTICA_MODIFICADA
        return HEURISTICA_ORIGINAL

    def reiniciar(self):
        self.heuristica = self.pegar_heuristica()

        # Começamos apenas com a Base disponível.
        self.disponiveis = [INICIO]

        # Visitados são os estados que já foram encontrados.
        self.visitados = {INICIO}
        self.ordem_visita = [INICIO]

        # Expandidos são os estados que tiveram seus vizinhos analisados.
        self.expandidos = []

        # Guarda de onde cada estado veio para montar o caminho final.
        self.predecessor = {INICIO: None}

        self.atual = None
        self.passo = 0
        self.finalizado = False
        self.encontrou = False

        self.lbl_passo.config(text="Passo: 0")
        self.lbl_atual.config(text="Estado atual: -")
        self.lbl_novos.config(text="Novos estados: -")
        self.lbl_proximo.config(text=f"Próximo: {INICIO}")
        self.lbl_explicacao.config(
            text="A busca começa com a Base de Atendimento. Em cada passo, é escolhido o estado disponível com menor h(n)."
        )

        self.atualizar_disponiveis()
        self.atualizar_resultado()
        self.desenhar()

    def ordenar_disponiveis(self):
        # Menor h(n) primeiro. Se empatar, usa ordem alfabética.
        return sorted(
            self.disponiveis,
            key=lambda estado: (self.heuristica[estado], estado)
        )

    def proximo_passo(self, mostrar_mensagem=True):
        if self.finalizado:
            return

        if not self.disponiveis:
            self.finalizado = True
            self.lbl_explicacao.config(text="Não existem mais estados disponíveis.")
            return

        self.passo += 1

        # Antes de escolher, ordenamos TODOS os estados disponíveis pelo h(n).
        candidatos = self.ordenar_disponiveis()
        self.atual = candidatos[0]
        self.disponiveis.remove(self.atual)

        self.lbl_passo.config(text=f"Passo: {self.passo}")
        self.lbl_atual.config(text=f"Estado atual: {self.atual}")

        # Se o estado escolhido for o hospital, terminamos a busca.
        if self.atual == OBJETIVO:
            self.finalizado = True
            self.encontrou = True
            self.lbl_novos.config(text="Novos estados: nenhum")
            self.lbl_proximo.config(text="Próximo: -")
            self.lbl_explicacao.config(
                text=f"{OBJETIVO} foi escolhido porque possui h(n)=0. Objetivo encontrado!"
            )
            self.atualizar_disponiveis()
            self.atualizar_resultado()
            self.desenhar()

            if mostrar_mensagem:
                messagebox.showinfo("Busca finalizada", "Hospital Central encontrado!")
            return

        novos = []

        # Analisa os vizinhos do estado atual.
        for vizinho in GRAFO[self.atual]:
            if vizinho not in self.visitados:
                self.visitados.add(vizinho)
                self.ordem_visita.append(vizinho)
                self.disponiveis.append(vizinho)
                self.predecessor[vizinho] = self.atual
                novos.append(vizinho)

        self.expandidos.append(self.atual)

        # Descobre qual será o próximo estado, considerando todos os disponíveis.
        ordenados_depois = self.ordenar_disponiveis()
        proximo = ordenados_depois[0] if ordenados_depois else None

        if novos:
            texto_novos = ", ".join(novos)
        else:
            texto_novos = "nenhum"

        self.lbl_novos.config(text=f"Novos estados: {texto_novos}")
        self.lbl_proximo.config(text=f"Próximo: {proximo if proximo else '-'}")

        texto_candidatos = self.formatar_estados(candidatos)
        self.lbl_explicacao.config(
            text=(
                f"Candidatos: {texto_candidatos}.\n"
                f"Foi escolhido {self.atual}, pois possui o menor h(n)."
            )
        )

        self.atualizar_disponiveis()
        self.atualizar_resultado()
        self.desenhar()

    def executar_tudo(self):
        while not self.finalizado:
            self.proximo_passo(mostrar_mensagem=False)

        if self.encontrou:
            messagebox.showinfo("Busca finalizada", "Hospital Central encontrado!")

    def montar_caminho(self):
        if not self.encontrou:
            return []

        caminho = []
        estado = OBJETIVO

        while estado is not None:
            caminho.append(estado)
            estado = self.predecessor[estado]

        caminho.reverse()
        return caminho

    def formatar_estados(self, estados):
        if not estados:
            return "nenhum"

        partes = []
        for estado in estados:
            partes.append(f"{estado} h={self.heuristica[estado]}")

        return ", ".join(partes)

    def atualizar_disponiveis(self):
        estados = self.ordenar_disponiveis()

        self.txt_disponiveis.delete("1.0", tk.END)
        self.txt_disponiveis.insert(tk.END, self.formatar_estados(estados))

    def atualizar_resultado(self):
        caminho = self.montar_caminho()

        if self.encontrou:
            status = "Objetivo encontrado"
            texto_caminho = " -> ".join(caminho)
        else:
            status = "Em execução"
            texto_caminho = "-"

        texto = (
            f"Status: {status}\n"
            f"Origem: {INICIO}\n"
            f"Destino: {OBJETIVO}\n\n"
            f"Ordem de visita:\n{' -> '.join(self.ordem_visita)}\n\n"
            f"Ordem de expansão:\n{' -> '.join(self.expandidos) if self.expandidos else '-'}\n\n"
            f"Caminho encontrado:\n{texto_caminho}\n\n"
            f"Visitados: {len(self.ordem_visita)}\n"
            f"Expandidos: {len(self.expandidos)}"
        )

        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, texto)

    def nome_curto(self, estado):
        nomes = {
            "Base de Atendimento": "Base",
            "Parque Municipal": "Parque",
            "Terminal Norte": "Terminal",
            "Praça Central": "Praça",
            "Beco Histórico": "Beco",
            "Ponte Central": "Ponte",
            "Hospital Central": "Hospital"
        }

        if estado in nomes:
            return nomes[estado]
        return estado

    def desenhar(self):
        self.canvas.delete("all")

        modo = "ORIGINAL" if self.tipo_heuristica.get() == "original" else "MODIFICADA"

        self.canvas.create_text(
            20,
            20,
            anchor="w",
            text=f"Mapa urbano - Heurística {modo}",
            font=("Arial", 16, "bold")
        )

        # Desenha as conexões.
        for origem, destino in CONEXOES:
            x1, y1 = POSICOES[origem]
            x2, y2 = POSICOES[destino]

            self.canvas.create_line(
                x1, y1, x2, y2,
                width=3,
                fill="gray"
            )

        # Desenha os estados.
        for estado, (x, y) in POSICOES.items():
            cor = "white"

            if estado in self.visitados:
                cor = "gold"

            if estado in self.expandidos:
                cor = "lightgray"

            if estado == self.atual:
                cor = "orange"

            if estado == OBJETIVO and self.encontrou:
                cor = "lightgreen"

            self.canvas.create_oval(
                x - 70,
                y - 32,
                x + 70,
                y + 32,
                fill=cor,
                outline="black",
                width=2
            )

            self.canvas.create_text(
                x,
                y - 8,
                text=self.nome_curto(estado),
                font=("Arial", 10, "bold")
            )

            self.canvas.create_text(
                x,
                y + 12,
                text=f"h(n)={self.heuristica[estado]}",
                font=("Arial", 9)
            )

        self.canvas.create_text(
            20,
            590,
            anchor="w",
            text="Amarelo = visitado | Laranja = atual | Cinza = expandido | Verde = objetivo",
            font=("Arial", 10)
        )


if __name__ == "__main__":
    janela = tk.Tk()
    app = BuscaHeuristicaVisual(janela)
    janela.mainloop()
