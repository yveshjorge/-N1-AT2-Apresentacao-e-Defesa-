# Guia rápido para a apresentação em sala

## Explicação em 2–3 minutos

1. **Problema:** a Base de Atendimento precisa chegar ao Hospital Central usando um mapa representado por grafo.
2. **Grafo:** existem 12 estados e 19 conexões. Há vários caminhos até o Hospital e o **Beco Histórico** é um estado sem saída.
3. **Heurística:** `h(n)` estima a proximidade ao Hospital. Quanto menor, mais promissor o estado parece. Hospital tem `h=0`.
4. **Algoritmo:** a busca mantém todos os estados disponíveis em uma fronteira. Ela sempre escolhe o menor `h(n)`. Em empate, usa ordem alfabética.
5. **Visitados:** impedem repetição/ciclos. Um estado vira visitado quando é descoberto e colocado na busca.
6. **Predecessores:** registram de onde cada estado veio. No final, permitem reconstruir o caminho do Hospital até a Base.
7. **Primeira execução:** Base → Parque → Universidade. O algoritmo cai no Beco Histórico porque ele tem `h=2`, percebe que ele não possui nenhum vizinho novo e então escolhe o próximo candidato que já estava na lista. Depois seleciona a Ponte e o Hospital.
8. **Segunda execução:** mudamos apenas Centro, Parque e Universidade. A busca passa por Centro → Praça → Ponte → Hospital.
9. **Comparação:** original = 12 visitados e 5 expandidos; modificada = 11 visitados e 4 expandidos. A heurística mudou a ordem e o caminho.

## Perguntas que o professor pode fazer

**Por que não é uma rota fixa?**  
Porque o próximo estado é calculado em tempo de execução a partir de todos os estados disponíveis e de seus valores `h(n)`.

**Onde está a regra do menor h?**  
No método `ordenar_disponiveis()`, que ordena por `(heuristica[estado], estado)`.

**Como funciona o empate?**  
Se dois estados têm o mesmo `h`, o segundo item da ordenação é o nome do estado, então vence a ordem alfabética.

**Para que serve `visitados`?**  
Evita descobrir/adicionar o mesmo estado várias vezes, impedindo ciclos e expansões repetidas.

**Para que serve `predecessor`?**  
Guarda o estado anterior de cada novo nó. Quando o Hospital é encontrado, `montar_caminho()` volta pelos predecessores até a Base.

**Qual a diferença entre visitado e expandido neste projeto?**  
Visitado = descoberto e adicionado à busca. Expandido = selecionado e teve os vizinhos examinados. O Hospital é selecionado, mas não precisa ser expandido.

**Por que o Beco Histórico é importante?**  
Ele prova que um valor heurístico baixo não garante que exista um caminho direto. Ele parece muito próximo do Hospital (`h=2`), mas é sem saída.

**A busca olha apenas os vizinhos do último estado?**  
Não. Todos os candidatos ainda não explorados ficam na lista `disponiveis` e continuam sendo comparados nos passos seguintes.

## Como rodar na apresentação

```bash
python main.py
```

- Comece em **Original**.
- Clique em **Próximo passo** e mostre os candidatos e o Beco Histórico.
- Depois clique em **Reiniciar**, escolha **Modificada** e execute novamente.
- Mostre que o caminho e as quantidades mudam.
