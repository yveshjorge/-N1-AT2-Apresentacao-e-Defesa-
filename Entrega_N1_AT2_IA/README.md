# N1 – AT2 – Inteligência Artificial I
## Busca Heurística para rota de emergência

Projeto em Python inspirado na organização visual do exemplo de aula do professor, porém implementando **Busca Heurística (Greedy Best-First Search)** conforme o enunciado da atividade.

### Cenário
- Origem: **Base de Atendimento**
- Destino: **Hospital Central**
- 12 estados
- 19 conexões
- vários caminhos possíveis até o hospital
- estado sem saída: **Beco Histórico**
- o Beco Histórico possui h(n) baixo e parece promissor, mas é um beco sem saída
- critério de desempate: **ordem alfabética**

### Heurística
A heurística original representa uma estimativa aproximada da distância em linha reta, em quilômetros, até o Hospital Central. O Hospital possui `h(n) = 0`.

Na segunda execução, somente três valores são alterados propositalmente:

| Estado | Original | Modificada |
|---|---:|---:|
| Centro | 10 | 4 |
| Parque Municipal | 7 | 13 |
| Universidade | 5 | 11 |

### Como executar
Requisito: Python 3 com Tkinter.

Interface visual:

```bash
python main.py
```

### O que a interface mostra
- mapa completo do grafo;
- h(n) de todos os estados;
- estados visitados/descobertos;
- estado selecionado;
- estados expandidos;
- novos estados encontrados;
- lista global de estados disponíveis ordenada por h(n);
- próximo estado escolhido;
- ordem de visita;
- ordem de expansão;
- caminho reconstruído pelos predecessores;
- quantidade de visitados e expandidos;
- troca entre heurística original e modificada.

### Observação sobre o repositório
A atividade pede um link de GitHub ou equivalente. Este pacote está pronto para ser enviado a um repositório. Depois de publicar, substitua o campo **[INSERIR LINK DO REPOSITÓRIO]** no relatório.
