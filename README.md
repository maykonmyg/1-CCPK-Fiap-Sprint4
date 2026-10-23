# LightWeek — Sprint 4

Continuação da Sprint 3 de Data Structures and Algorithms, turma 1CCPK.
O código original de `sistema_recarga.py` foi preservado. A nova interface Web usa suas funções Python.

## Como abrir

1. Extraia o ZIP inteiro para uma pasta.
2. Com Python 3 instalado, abra o terminal nessa pasta e execute `python app.py` (ou `py app.py`).
3. Abra http://127.0.0.1:8765 no navegador.
4. Mantenha o terminal aberto enquanto usa o sistema. Encerre com Ctrl+C.

Não há bibliotecas externas obrigatórias. Não abra `web/index.html` diretamente: a interface depende do servidor Python.

## O que está incluído

- Interface Web: cadastro, listagem, busca por ID, ordenação por ID/energia/custo/tempo, estatísticas e resumo final.
- Backend Python: classe Sessao, lista de objetos, busca sequencial e Insertion Sort manual da Sprint 3.
- Custo calculado no Python por energia × tarifa, sem aceitar custo enviado pela interface.
- Validação de IDs repetidos, números inválidos/negativos, campos e datas.
- Área técnica com trechos extraídos das funções Python realmente utilizadas.
- Apresentação da equipe, evolução, complexidade e duas propostas futuras.
- Roteiro sugerido de 6min30 para os cinco integrantes narrarem e demonstrarem.

## Limites e verificação

O armazenamento é em memória e se perde ao encerrar/reiniciar o servidor. A aplicação é didática e local; não é um servidor de produção. Valores monetários mantêm os floats do projeto original e são exibidos com duas casas decimais. O valor acumulado inclui sessões em andamento.

Os testes originais e os testes adicionais do backend foram executados. A comunicação HTTP no navegador e a aparência final NÃO foram verificadas neste ambiente: a conexão local foi bloqueada e a execução fora do isolamento foi recusada. O vídeo NÃO foi produzido. O roteiro é uma preparação para a gravação, não uma evidência de gravação já realizada.

Para testar: `python -m unittest discover -s tests -v`.

## Entrega ao professor

Exclusivamente o link de um vídeo de 5 a 8 minutos no YouTube, Público ou Não listado. Acrescentar a narração dos integrantes antes da publicação. Todos devem explicar pelo menos uma parte técnica. Testar o link em janela anônima e manter acessível até o fim da avaliação.

## Equipe informada no README anterior

- Maykon de Lima Silva — RM 574022
- Felipe Pereira Restivo — RM 570712
- Gabriel Rodrigues Zappelloni — RM 572060
- Rodger Costa Rios — RM 571438
- Kenichi Caio Yamamoto — RM 569815

Confiram os dados antes da gravação. O histórico das Sprints 1 e 2 não foi fornecido; não foram inventados detalhes dessas etapas.
