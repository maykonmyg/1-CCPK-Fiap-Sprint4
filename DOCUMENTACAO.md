# Documentação técnica — Sprint 4

## Relação com o projeto anterior

O README fornecido identifica explicitamente a Sprint 3 de Data Structures and Algorithms. O enunciado da Sprint 4 pede finalizar o projeto do semestre e apresentar a evolução. Logo, este é o projeto-base adequado. Os arquivos das Sprints 1 e 2 não foram recebidos; a descrição anterior de um simulador de recarga vem da documentação da Sprint 3.

## Arquitetura

`web/index.html` apresenta formulários e tabelas. `web/app.js` usa fetch para enviar e receber JSON. `app.py` fornece os arquivos da interface e as rotas da API usando a biblioteca padrão do Python. `sistema_recarga.py` contém a classe e os algoritmos reaproveitados da Sprint 3.

| Ação | Rota | Processamento Python |
|---|---|---|
| Cadastro | POST /api/sessoes | Valida, busca ID duplicado, cria Sessao, adiciona à lista |
| Listagem e estatísticas | GET /api/sessoes | Serializa a lista e chama calcular_estatisticas |
| Busca | GET /api/busca?id=10 | Chama busca_sequencial e retorna objeto ou ausência |
| Ordenação | POST /api/ordenar | Chama insertion_sort com critério e direção |
| Código técnico | GET /api/codigo | inspect.getsource extrai as funções efetivamente usadas |

Fluxo: interface → HTTP/JSON → Python → processamento → JSON → interface.

## Estruturas e complexidade

Cada Sessao reúne ID, veículo, tipo de carregador, energia, tempo, tarifa, data, status e custo. Uma lista contém vários objetos; `append` acrescenta uma referência. A lista mantém ordem e permite aplicar os algoritmos da disciplina diretamente.

| Operação | Tempo | Motivo |
|---|---|---|
| Cálculo de custo | O(1) | Uma multiplicação de energia por tarifa |
| append | O(1) amortizado | Expansões ocasionais da capacidade da lista |
| Cadastro completo | O(n) | Antes de append, busca duplicidade percorrendo a lista |
| Busca sequencial | Melhor O(1); médio/pior O(n) | Pode parar no primeiro item ou verificar todos |
| Insertion Sort | Melhor O(n); médio/pior O(n²) | Desloca elementos anteriores até a posição correta |
| Estatísticas/listagem | O(n) | Percorre todos os registros |

Busca e Insertion Sort usam espaço auxiliar O(1), desconsiderando a lista de entrada. Serializar a lista para responder à interface cria uma representação adicional O(n). Armazenar n sessões ocupa O(n).

A busca compara IDs e retorna o índice do primeiro correspondente, ou -1 se não houver. A ordenação aceita ID, energia, custo e tempo; compara com > na ordem crescente e < na decrescente. Valores iguais preservam a ordem relativa, tornando esta implementação estável. Não usa sort/ sorted para substituir o algoritmo manual.

Em ordem inversa, o Insertion Sort realiza n(n−1)/2 deslocamentos: 45 para n=10, 190 para n=20 e 780 para n=40. A busca sem sucesso faz n comparações. Esses números ilustram operações, não medições de tempo de execução.

O(log n) e O(n log n) não são complexidades dos algoritmos de busca e ordenação implementados. Uma futura busca binária exigiria ordenação pela chave; um futuro Merge Sort teria tempo O(n log n) com custos adicionais de memória na implementação convencional.

## Resumo e limites

O resumo calcula quantidade, energia total, valor total, média, maior e menor consumo. Os custos são energia × tarifa e mantêm o tipo float da versão original. O painel não simula fisicamente a transferência de energia: registra sessões informadas pelo usuário. Não há conexão com carregadores reais.

O estado é uma lista em memória no processo Python. Recarregar a página preserva os dados enquanto esse processo continuar; reiniciar o servidor os perde. Persistência em banco e múltiplas estações são duas evoluções propostas, não implementadas.

## Validação realizada

Onze testes automatizados de lógica Python passaram: os cinco originais e seis adicionais, incluindo fluxo de três sessões, rejeição de duplicados/valores inválidos, datas, vírgula decimal e estabilidade da ordenação. A sintaxe do JavaScript também foi conferida.

A conexão navegador-servidor foi bloqueada pelo ambiente de execução. Não foi possível concluir o teste visual nem produzir o vídeo. Executar e conferir a interface localmente antes da gravação continua pendente.
