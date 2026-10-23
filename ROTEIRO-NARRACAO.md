LIGHTWEEK — EXPLICAÇÃO DE CADA PÁGINA

Texto de apoio para entender o sistema e explicar suas telas.
Referente à versão atual, com as abas Projeto, Estação, Código Python, Complexidade e Evolução.


1. PROJETO

Esta é a página de apresentação do LightWeek. Ela explica o problema que o sistema busca resolver: organizar várias sessões de recarga, consultar seus dados e acompanhar o consumo de energia e os custos.

A tela apresenta a disciplina Data Structures and Algorithms, a turma 1CCPK e a equipe com os nomes completos e RMs dos integrantes.

Também mostra a evolução do projeto. A documentação anterior descreve um simulador de recarga que evoluiu, na Sprint 3, para um programa de terminal capaz de cadastrar, buscar, ordenar e analisar várias sessões. Na Sprint 4, esse código recebeu uma interface Web conectada ao Python.

A interface Web é a parte que o usuário vê no navegador. O backend é a parte em Python que recebe os pedidos, processa os dados e devolve os resultados. Os registros ficam na memória do programa enquanto o servidor está funcionando.

Esta página ajuda a apresentar o contexto do trabalho. Ela não realiza cadastros nem cálculos.


2. ESTAÇÃO

Esta é a principal página de uso do sistema. Nela, o usuário cadastra sessões de recarga, consulta registros, faz buscas, ordena os dados e acompanha estatísticas.

NOVA SESSÃO

O botão “Nova sessão” abre um formulário com os seguintes campos:

- ID: número inteiro positivo que identifica a sessão e não pode se repetir.
- Veículo: identificação do veículo associado à recarga.
- Carregador: tipo de carregador utilizado, com opções lento, rápido e ultrarrápido.
- Data: dia em que a sessão foi registrada.
- Energia: quantidade de energia informada, em quilowatts-hora, ou kWh.
- Tempo: duração informada da recarga, em minutos.
- Tarifa: preço por quilowatt-hora, em reais.
- Status: indica se a sessão está finalizada ou em andamento.

Ao clicar em “Cadastrar e calcular custo”, a página envia os dados ao Python. O backend verifica as informações, cria um objeto da classe Sessao e o acrescenta à lista de registros.

O custo é calculado pelo Python multiplicando a energia pela tarifa. Por exemplo: 20 kWh multiplicados por R$ 1,50 por kWh resultam em R$ 30,00. O usuário não digita o custo final.

O sistema registra os valores preenchidos. Ele não se conecta a um carregador real, não mede energia automaticamente e não calcula a energia a partir da potência do carregador e do tempo. O status “Em andamento” é uma informação do cadastro, não uma recarga acompanhada em tempo real.

INDICADORES

Os quatro indicadores mostram:

- Sessões armazenadas: quantidade de registros na lista.
- Energia fornecida: soma da energia informada em todas as sessões.
- Valor acumulado: soma dos custos das sessões.
- Custo médio: valor acumulado dividido pela quantidade de sessões.

Essas informações são calculadas com os registros atuais. Sessões marcadas como “Em andamento” também entram nos totais; portanto, o valor acumulado não representa necessariamente pagamentos já recebidos.

LISTAGEM

A tabela exibe ID, veículo, carregador, energia, tempo, custo e status de cada sessão. Ela permite visualizar vários registros ao mesmo tempo.

BUSCAR POR ID

O usuário informa o ID e clica em “Buscar”. O Python executa a busca sequencial, comparando os IDs da lista até encontrar a sessão ou chegar ao fim.

Se encontrar, a página destaca a linha correspondente e informa o resultado e a quantidade de comparações. Se não encontrar, apresenta uma mensagem. A busca não remove os outros registros da tabela.

ORDENAR

O usuário escolhe um campo — ID, energia, custo ou tempo — e a direção crescente ou decrescente. Ao clicar em “Ordenar”, o Python executa o Insertion Sort implementado manualmente no projeto e a tabela apresenta a nova sequência.

Por exemplo, ordenar por custo crescente coloca primeiro a sessão de menor custo. Ordenar por energia decrescente coloca primeiro a sessão de maior consumo.

VER RESUMO FINAL

Esse botão exibe um resumo com quantidade de sessões, energia total, valor acumulado, custo médio, menor consumo e maior consumo. O resumo aparece na própria página; o botão não gera um arquivo para download.

ARMAZENAMENTO

Os registros são mantidos em uma lista de objetos na memória do Python. Atualizar a página não apaga os dados enquanto o mesmo servidor continua funcionando. Encerrar ou reiniciar o servidor perde esses registros, pois esta versão não possui banco de dados.


3. CÓDIGO PYTHON

Esta página serve de apoio à defesa técnica. Ela mostra trechos extraídos das funções Python realmente utilizadas pelo servidor, permitindo relacionar o funcionamento da interface ao código.

Os botões alternam entre cinco partes:

CLASSE SESSAO

A classe representa uma sessão de recarga. Cada objeto reúne ID, veículo, tipo de carregador, energia, tempo, tarifa, data, status e custo.

Essa estrutura mantém juntas as informações da mesma recarga. Uma lista armazena vários desses objetos, permitindo trabalhar com múltiplas sessões sem criar listas separadas para cada campo.

O custo é calculado no momento em que o objeto é criado, por meio da multiplicação entre energia e tarifa.

CADASTRO E INTEGRAÇÃO

Este trecho mostra a função que recebe os dados do cadastro. Ela verifica o ID, impede duplicidade, valida os campos e cria a sessão. Depois, utiliza append para acrescentar o objeto à lista e devolve seus dados.

O fluxo completo é: o navegador envia uma requisição HTTP com dados em JSON; o servidor Python recebe a requisição e chama a função de cadastro; o resultado volta em JSON; a interface atualiza a tabela e os indicadores.

HTTP é a forma de comunicação entre navegador e servidor. JSON é o formato usado para transportar os dados, organizados em campos e valores.

BUSCA SEQUENCIAL

A função recebe a lista e o ID procurado. Ela começa no primeiro registro e compara cada ID com a chave de busca.

Quando encontra uma correspondência, retorna o índice, ou posição, do registro na lista. Se chegar ao fim sem encontrar, retorna -1. Isso permite ao sistema distinguir uma sessão encontrada de uma busca sem resultado.

INSERTION SORT

Esse algoritmo ordena os registros manualmente. Ele considera a parte inicial da lista já ordenada, guarda a sessão atual e compara seu valor com os anteriores.

Quando um elemento anterior está na posição errada em relação à direção escolhida, ele é deslocado uma posição para a direita. Ao encontrar o lugar correto, o algoritmo insere a sessão que havia sido guardada.

As comparações dependem do critério selecionado: ID, energia, custo ou tempo. O sentido das comparações muda conforme a ordem crescente ou decrescente. A implementação não substitui o algoritmo por sort() ou sorted().

ESTATÍSTICAS

A função percorre a lista, somando a energia e os custos e acompanhando o maior e o menor consumo. Depois, calcula o custo médio dividindo o total pela quantidade de sessões.

Quando a lista está vazia, a função retorna None para indicar que ainda não existem dados para calcular as estatísticas. A interface trata essa situação e mostra indicadores zerados.


4. COMPLEXIDADE

Esta página explica como a quantidade de operações cresce quando aumenta o número de sessões. A letra n representa a quantidade de registros na lista.

A notação Big-O descreve o crescimento do trabalho do algoritmo. Ela não informa diretamente quantos segundos uma operação vai demorar.

O(1) — TEMPO CONSTANTE

O cálculo de uma sessão, energia multiplicada pela tarifa, realiza uma multiplicação independentemente de quantos registros existem. Por isso, é O(1).

A busca também tem melhor caso O(1): isso acontece quando o ID procurado está logo no primeiro registro.

O(n) — CRESCIMENTO LINEAR

No pior caso, a busca sequencial precisa comparar todos os IDs. Com 10 sessões, pode fazer 10 comparações; com 20, pode fazer 20; com 40, pode fazer 40. Dobrar a quantidade de registros dobra o limite de comparações.

O pior caso ocorre quando o registro está no fim ou não existe. O caso médio da busca também é O(n).

As estatísticas são O(n), pois precisam percorrer a lista para considerar todas as sessões.

O Insertion Sort tem melhor caso O(n), quando a lista já está na ordem desejada: ainda é necessário passar pelos itens, mas quase não há trabalho no laço interno e não há deslocamentos.

O(n²) — CRESCIMENTO QUADRÁTICO

O Insertion Sort tem pior caso O(n²), quando a lista está na ordem inversa à desejada. Cada item pode precisar atravessar toda a parte anterior da lista.

Nessa situação, a quantidade de deslocamentos é n × (n - 1) / 2. Para 10 registros, são 45 deslocamentos; para 20, são 190; para 40, são 780.

Ao dobrar n, essa quantidade se aproxima de quatro vezes a anterior. O caso médio do Insertion Sort também é O(n²).

Os números apresentados são contagens teóricas de comparações ou deslocamentos nas situações descritas, não medições do tempo de execução do computador.

O(log n) E O(n log n)

Essas notações aparecem para contextualizar outras possibilidades. Elas não representam a busca e a ordenação implementadas nesta versão.

Uma busca binária pode ter tempo O(log n), mas precisa de dados organizados pela chave de busca. O Merge Sort é uma alternativa de ordenação com tempo O(n log n). Nenhum desses dois algoritmos foi implementado neste projeto.


5. EVOLUÇÃO

Esta página apresenta a comunicação entre as partes do sistema e duas possíveis melhorias futuras.

COMUNICAÇÃO ENTRE INTERFACE E BACKEND

O fluxo mostrado é:

Navegador -> requisição HTTP com JSON -> processamento em Python -> resposta -> atualização da interface.

O usuário interage com campos e botões no navegador. O Python recebe os pedidos, manipula a lista de objetos, executa os algoritmos e devolve os resultados. A página apresenta essas respostas em tabelas, mensagens e indicadores.

EVOLUÇÃO 1: PERSISTÊNCIA

A primeira proposta é acrescentar um banco de dados para preservar o histórico mesmo depois que o servidor for encerrado ou reiniciado.

Hoje, os dados existem apenas na memória do programa. A persistência permitiria recuperar as sessões em uma próxima execução. Essa melhoria é uma proposta e ainda não está implementada.

EVOLUÇÃO 2: MÚLTIPLAS ESTAÇÕES

A segunda proposta é associar cada sessão a uma estação específica. Assim, seria possível acompanhar o consumo e os valores de cada local e também gerar resultados consolidados.

Uma integração com carregadores reais poderia ser desenvolvida em uma etapa posterior. Essas funcionalidades também não estão implementadas na versão atual.

ENCERRAMENTO

A página retoma o que o sistema oferece: cadastro, listagem, busca sequencial, ordenação manual, estatísticas, tarifação e resumo final.

As páginas Projeto, Código Python, Complexidade e Evolução são recursos de apoio à apresentação. O enunciado exige explicar esses assuntos no vídeo, mas não exige que existam abas específicas para eles dentro do site.
