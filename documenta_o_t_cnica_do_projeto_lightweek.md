# Documentação Técnica e Funcional — LightWeek (Sprint 4)

**Turma:** 1CCPK  
**Projeto:** LightWeek — Sistema de Gestão e Simulação de Recargas para Veículos Elétricos  

---

## 1. Integrantes da Equipe

| Nome do Integrante | RM |
| :--- | :--- |
| **Maykon de Lima Silva** | 574022 |
| **Felipe Pereira Restivo** | 570712 |
| **Gabriel Rodrigues Zappelloni** | 572060 |
| **Rodger Costa Rios** | 571438 |
| **Kenichi Caio Yamamoto** | 569815 |

---

## 2. Visão Geral do Projeto

O **LightWeek** é um sistema desenvolvido para gerenciar, registrar e analisar sessões de recarga de veículos elétricos. Ele evoluiu de um simulador em modo terminal (Sprint 3) para uma aplicação Web completa (Sprint 4) com arquitetura cliente-servidor, mantendo todas as regras de negócio, manipulação de dados e algoritmos implementados estritamente em Python.

### Principais Objetivos
* Registrar sessões de recarga controlando identificadores únicos (ID), veículos, potência de carregadores, consumo energético, tempo de sessão e tarifas aplicadas.
* Calcular custos dinamicamente no backend, impedindo adulteração de valores pela interface.
* Disponibilizar buscas por identificador e ordenação customizada por múltiplos critérios.
* Exibir estatísticas consolidadas (faturamento total, média de custos, consumo máximo e mínimo).
* Demonstrar o uso prático de estruturas de dados e algoritmos clássicos de ordenação e busca manual.

---

## 3. Arquitetura do Sistema

A aplicação adota o padrão de comunicação desacoplado **Interface Web $\leftrightarrow$ API REST em Python (Backend)**.

```
+-------------------------------------------------------+
|                 Navegador Web (SPA)                   |
|       (index.html / style.css / app.js)               |
+-------------------------------------------------------+
                           |
                     Requisição HTTP (JSON)
                           v
+-------------------------------------------------------+
|                 Servidor Python Local                 |
|       (app.py - ThreadingHTTPServer / Handler)        |
+-------------------------------------------------------+
                           |
                Invocação das Regras
                           v
+-------------------------------------------------------+
|            Módulo de Lógica e Algoritmos              |
|   (sistema_recarga.py - Classe Sessao e Algoritmos)  |
+-------------------------------------------------------+
```

### Tecnologias Utilizadas
* **Backend:** Python 3 (Bibliotecas nativas `http.server`, `json`, `inspect`, `pathlib`, `datetime`). Não requer instalação de dependências externas.
* **Frontend:** HTML5, CSS3 (layout responsivo com CSS Grid/Flexbox) e JavaScript Vanilla (`fetch` API).
* **Armazenamento:** Em memória RAM (lista de objetos Python durante o ciclo de vida do servidor).

---

## 4. Estruturas de Dados e Algoritmos (Python)

### 4.1. Representação do Dado (`Sessao`)
Cada sessão de recarga é representada por uma instância da classe `Sessao` (no arquivo `sistema_recarga.py`).

**Atributos:**
* `id` *(int)*: Identificador único da sessão (chave primária).
* `veiculo` *(str)*: Modelo/identificação do veículo elétrico.
* `tipo_carregador` *(str)*: Categoria do carregador (*Lento - 7,4 kW*, *Rápido - 22 kW*, *Ultrarrápido - 50 kW*).
* `energia_kwh` *(float)*: Total de energia consumida em kWh.
* `tempo_minutos` *(float)*: Duração total da recarga em minutos.
* `tarifa_kwh` *(float)*: Valor cobrado por kWh (R$/kWh).
* `data` *(str)*: Data do registro.
* `status` *(str)*: *Finalizada* ou *Em andamento*.
* `custo` *(float)*: Atributo calculado no backend ($custo = energia\_kwh \times tarifa\_kwh$).

### 4.2. Armazenamento
Os dados são armazenados na lista global `sessoes = []` no arquivo `app.py`. A inserção de novos itens utiliza o método `.append()`, mantendo a ordem cronológica do cadastro.

### 4.3. Algoritmo de Busca (`busca_sequencial`)
Para localizar um registro específico, utiliza-se a **Busca Sequencial**.

```python
def busca_sequencial(sessoes, id_procurado):
    for indice in range(len(sessoes)):
        if sessoes[indice].id == id_procurado:
            return indice
    return -1
```
* **Chave de Busca:** ID único da sessão.
* **Funcionamento:** Percorre a lista elemento por elemento até encontrar um objeto cujo `.id` seja igual a `id_procurado`. Retorna a posição (índice) do elemento ou `-1` se não for localizado.

### 4.4. Algoritmo de Ordenação (`insertion_sort`)
Atendendo aos requisitos acadêmicos, a ordenação é feita utilizando o algoritmo **Insertion Sort** (sem uso de `sort()` ou `sorted()`).

```python
def insertion_sort(sessoes, criterio, crescente=True):
    for i in range(1, len(sessoes)):
        sessao_atual = sessoes[i]
        valor_atual = obter_valor_criterio(sessao_atual, criterio)
        j = i - 1

        while j >= 0:
            valor_anterior = obter_valor_criterio(sessoes[j], criterio)

            if crescente:
                precisa_mover = valor_anterior > valor_atual
            else:
                precisa_mover = valor_anterior < valor_atual

            if not precisa_mover:
                break

            sessoes[j + 1] = sessoes[j]
            j -= 1

        sessoes[j + 1] = sessao_atual
```
* **Critérios Suportados:** 1 (ID), 2 (Energia consumida), 3 (Custo total) e 4 (Tempo de recarga).
* **Funcionamento:** Algoritmo in-place e estável. Percorre a lista a partir do segundo elemento, comparando o valor atual com os elementos anteriores e deslocando-os para a direita até encontrar a posição correta.

---

## 5. Análise de Complexidade Computacional (Big-O)

| Operação | Algoritmo / Estrutura | Complexidade de Tempo (Melhor Caso) | Complexidade de Tempo (Pior Caso) | Complexidade de Espaço |
| :--- | :--- | :--- | :--- | :--- |
| **Cálculo de Tarifação** | Atribuição Direta ($E \times T$) | $O(1)$ | $O(1)$ | $O(1)$ |
| **Inserção na Lista** | `list.append()` | $O(1)$ (amortizado) | $O(1)$ | $O(1)$ |
| **Busca por ID** | Busca Sequencial | $O(1)$ *(primeiro item)* | $O(n)$ *(não encontra ou último item)* | $O(1)$ |
| **Ordenação de Sessões** | Insertion Sort | $O(n)$ *(lista já ordenada)* | $O(n^2)$ *(lista em ordem inversa)* | $O(1)$ |
| **Estatísticas Globais** | Laço Único ($1$ passagem) | $O(n)$ | $O(n)$ | $O(1)$ |

### Explicação Detalhada

* **Tempo Constante $O(1)$:** O cálculo do custo de recarga e o acesso direto a atributos acontecem instantaneamente, independentemente do número $n$ de sessões gravadas.
* **Tempo Linear $O(n)$:** A busca sequencial precisa comparar chave por chave. Caso $n$ dobre de tamanho (ex: de 10 para 20 sessões), o número máximo de verificações no pior caso também dobra (de 10 para 20).
* **Tempo Quadrático $O(n^2)$:** No Insertion Sort, com a lista totalmente desordenada de forma inversa, o número de trocas/deslocamentos aproxima-se de $\frac{n(n-1)}{2}$. Para $n=10$, ocorrem até 45 deslocamentos; para $n=40$, o número sobe para 780 deslocamentos.

---

## 6. Endpoints da API HTTP (`app.py`)

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Retorna o arquivo principal da interface Web (`index.html`). |
| `GET` | `/api/sessoes` | Retorna a lista de todas as sessões cadastradas e o objeto de estatísticas. |
| `POST` | `/api/sessoes` | Cadastra uma nova sessão enviando os dados em JSON. Retorna o objeto criado e o custo. |
| `GET` | `/api/busca?id=X` | Executa a busca sequencial pelo ID $X$ e retorna o resultado e a quantidade de comparações. |
| `POST` | `/api/ordenar` | Executa o `insertion_sort` na lista global com base no critério e direção especificados. |
| `GET` | `/api/codigo` | Retorna os códigos-fonte das funções Python do backend para exibição técnica no frontend. |

---

## 7. Como Executar o Projeto

### Pré-requisitos
* Python 3.8 ou superior instalado.

### Passo a Passo

1. Extraia o pacote ZIP para uma pasta local de sua preferência.
2. No Windows, você pode dar um duplo clique no arquivo **`INICIAR.bat`** ou abrir o terminal no diretório da aplicação.
3. Para iniciar via terminal, execute:
   ```bash
   python app.py
   ```
4. Abra o navegador de sua preferência e acesse o endereço:
   ```text
   http://127.0.0.1:8765
   ```
5. Mantenha o terminal aberto enquanto interage com a aplicação Web. Para finalizar o servidor, pressione `Ctrl + C` no terminal.

---

## 8. Testes Automatizados

O projeto possui uma suíte completa de testes unitários localizados na pasta `tests/`.

Para rodar todos os testes de lógica e integração do backend, execute o comando abaixo na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

**Cenários Testados:**
* Cálculo correto do custo ($energia \times tarifa$).
* Validação de IDs duplicados.
* Tratamento de entradas numéricas com vírgula, zeros ou valores inválidos (`NaN`, números negativos, etc.).
* Comportamento da busca sequencial para chaves existentes e inexistentes.
* Ordenação via Insertion Sort e verificação de estabilidade.
* Cálculo de estatísticas consolidadas.

---

## 9. Propostas de Evolução Futura

1. **Persistência em Banco de Dados:** Substituir a lista mantida em memória RAM por um banco de dados relacional (ex: SQLite ou PostgreSQL) ou NoSQL, garantindo a permanência do histórico de recargas após a reinicialização do servidor.
2. **Múltiplas Estações de Recarga:** Expandir o modelo de dados para vincular sessões a postos/pontos de recarga específicos, permitindo gerar estatísticas de faturamento regionalizadas e gerenciar múltiplos hubs concorrentemente.