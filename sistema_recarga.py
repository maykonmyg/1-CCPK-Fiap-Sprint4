from datetime import datetime


class Sessao:
    """Representa uma sessão de recarga armazenada pelo sistema."""

    def __init__(
        self,
        id_sessao,
        veiculo,
        tipo_carregador,
        energia_kwh,
        tempo_minutos,
        tarifa_kwh,
        data,
        status,
    ):
        self.id = id_sessao
        self.veiculo = veiculo
        self.tipo_carregador = tipo_carregador
        self.energia_kwh = energia_kwh
        self.tempo_minutos = tempo_minutos
        self.tarifa_kwh = tarifa_kwh
        self.data = data
        self.status = status
        self.custo = energia_kwh * tarifa_kwh


def busca_sequencial(sessoes, id_procurado):
    """Procura uma sessão pelo ID e devolve a posição dela na lista."""
    for indice in range(len(sessoes)):
        if sessoes[indice].id == id_procurado:
            return indice

    return -1


def obter_valor_criterio(sessao, criterio):
    """Escolhe qual valor será comparado pelo algoritmo de ordenação."""
    if criterio == 1:
        return sessao.id
    if criterio == 2:
        return sessao.energia_kwh
    if criterio == 3:
        return sessao.custo
    return sessao.tempo_minutos


def insertion_sort(sessoes, criterio, crescente=True):
    """Ordena a lista manualmente utilizando o algoritmo Insertion Sort."""
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


def ler_inteiro(mensagem, minimo=None, maximo=None):
    """Lê um número inteiro e não deixa o programa fechar por entrada inválida."""
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Digite um valor menor ou igual a {maximo}.")
                continue

            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_decimal(mensagem, minimo=None):
    """Lê um número decimal e aceita ponto ou vírgula."""
    while True:
        try:
            texto = input(mensagem).strip().replace(",", ".")
            valor = float(texto)

            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            return valor
        except ValueError:
            print("Entrada inválida. Digite um valor numérico.")


def ler_texto_obrigatorio(mensagem):
    """Impede que um campo de texto seja cadastrado vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Esse campo não pode ficar vazio.")


def escolher_carregador():
    print("\nTipo de carregador:")
    print("1 - Lento (7,4 kW)")
    print("2 - Rápido (22 kW)")
    print("3 - Ultrarrápido (50 kW)")

    opcao = ler_inteiro("Escolha: ", 1, 3)
    carregadores = {
        1: "Lento - 7,4 kW",
        2: "Rápido - 22 kW",
        3: "Ultrarrápido - 50 kW",
    }
    return carregadores[opcao]


def escolher_status():
    print("\nStatus da sessão:")
    print("1 - Finalizada")
    print("2 - Em andamento")

    opcao = ler_inteiro("Escolha: ", 1, 2)
    if opcao == 1:
        return "Finalizada"
    return "Em andamento"


def cadastrar_sessao(sessoes):
    print("\n========== NOVA SESSÃO ==========")

    while True:
        id_sessao = ler_inteiro("ID da sessão: ", 1)
        if busca_sequencial(sessoes, id_sessao) == -1:
            break
        print("Já existe uma sessão com esse ID. Digite outro.")

    veiculo = ler_texto_obrigatorio("Identificação do veículo: ")
    tipo_carregador = escolher_carregador()
    energia_kwh = ler_decimal("Energia consumida (kWh): ", 0)
    tempo_minutos = ler_decimal("Tempo de recarga (minutos): ", 0)
    tarifa_kwh = ler_decimal("Tarifa aplicada (R$/kWh): ", 0)

    data_digitada = input("Data da sessão (deixe vazio para usar hoje): ").strip()
    if data_digitada == "":
        data_digitada = datetime.now().strftime("%d/%m/%Y")

    status = escolher_status()

    nova_sessao = Sessao(
        id_sessao,
        veiculo,
        tipo_carregador,
        energia_kwh,
        tempo_minutos,
        tarifa_kwh,
        data_digitada,
        status,
    )
    sessoes.append(nova_sessao)

    print(f"\nSessão {id_sessao} cadastrada com sucesso.")
    print(f"Custo calculado: R$ {nova_sessao.custo:.2f}")


def exibir_sessao(sessao):
    """Exibe todos os dados de uma sessão de maneira organizada."""
    print(f"\nID: {sessao.id}")
    print(f"Veículo: {sessao.veiculo}")
    print(f"Carregador: {sessao.tipo_carregador}")
    print(f"Energia: {sessao.energia_kwh:.2f} kWh")
    print(f"Tempo: {sessao.tempo_minutos:.1f} minutos")
    print(f"Tarifa: R$ {sessao.tarifa_kwh:.2f}/kWh")
    print(f"Custo: R$ {sessao.custo:.2f}")
    print(f"Data: {sessao.data}")
    print(f"Status: {sessao.status}")


def listar_sessoes(sessoes):
    print("\n========================= SESSÕES CADASTRADAS =========================")

    if len(sessoes) == 0:
        print("Nenhuma sessão foi cadastrada até o momento.")
        return

    print(f"{'ID':<6}{'VEÍCULO':<22}{'ENERGIA':>12}{'TEMPO':>12}{'CUSTO':>13}")
    print("-" * 65)

    for sessao in sessoes:
        nome_veiculo = sessao.veiculo[:20]
        print(
            f"{sessao.id:<6}{nome_veiculo:<22}"
            f"{sessao.energia_kwh:>9.2f} kWh"
            f"{sessao.tempo_minutos:>8.1f} min"
            f"   R$ {sessao.custo:>7.2f}"
        )

    print(f"\nQuantidade armazenada: {len(sessoes)} sessão(ões).")


def buscar_sessao(sessoes):
    print("\n========== BUSCAR SESSÃO ==========")

    if len(sessoes) == 0:
        print("Não existem sessões cadastradas para pesquisar.")
        return

    id_procurado = ler_inteiro("Digite o ID da sessão: ", 1)
    posicao = busca_sequencial(sessoes, id_procurado)

    if posicao == -1:
        print("Sessão não encontrada.")
    else:
        print(f"Sessão encontrada na posição {posicao} da lista.")
        exibir_sessao(sessoes[posicao])


def ordenar_sessoes(sessoes):
    print("\n========== ORDENAR SESSÕES ==========")

    if len(sessoes) < 2:
        print("Cadastre pelo menos duas sessões para realizar a ordenação.")
        return

    print("1 - ID")
    print("2 - Energia consumida")
    print("3 - Custo")
    print("4 - Tempo de recarga")
    criterio = ler_inteiro("Ordenar por: ", 1, 4)

    print("\n1 - Ordem crescente")
    print("2 - Ordem decrescente")
    direcao = ler_inteiro("Escolha: ", 1, 2)

    insertion_sort(sessoes, criterio, direcao == 1)
    print("Sessões ordenadas manualmente com Insertion Sort.")
    listar_sessoes(sessoes)


def calcular_estatisticas(sessoes):
    """Calcula todas as estatísticas percorrendo a lista uma vez."""
    if len(sessoes) == 0:
        return None

    energia_total = 0
    faturamento_total = 0
    maior_consumo = sessoes[0].energia_kwh
    menor_consumo = sessoes[0].energia_kwh

    for sessao in sessoes:
        energia_total += sessao.energia_kwh
        faturamento_total += sessao.custo

        if sessao.energia_kwh > maior_consumo:
            maior_consumo = sessao.energia_kwh

        if sessao.energia_kwh < menor_consumo:
            menor_consumo = sessao.energia_kwh

    custo_medio = faturamento_total / len(sessoes)

    return {
        "quantidade": len(sessoes),
        "energia_total": energia_total,
        "faturamento_total": faturamento_total,
        "custo_medio": custo_medio,
        "maior_consumo": maior_consumo,
        "menor_consumo": menor_consumo,
    }


def mostrar_estatisticas(sessoes):
    print("\n========== ESTATÍSTICAS DA ESTAÇÃO ==========")
    dados = calcular_estatisticas(sessoes)

    if dados is None:
        print("Nenhuma sessão cadastrada para calcular as estatísticas.")
        return

    print(f"Sessões realizadas: {dados['quantidade']}")
    print(f"Energia fornecida: {dados['energia_total']:.2f} kWh")
    print(f"Faturamento total: R$ {dados['faturamento_total']:.2f}")
    print(f"Custo médio: R$ {dados['custo_medio']:.2f}")
    print(f"Maior consumo: {dados['maior_consumo']:.2f} kWh")
    print(f"Menor consumo: {dados['menor_consumo']:.2f} kWh")


def mostrar_menu():
    print("\n=====================================")
    print("     ESTAÇÃO DE RECARGA LIGHTWEEK")
    print("=====================================")
    print("1 - Nova sessão de recarga")
    print("2 - Listar sessões")
    print("3 - Buscar sessão")
    print("4 - Ordenar sessões")
    print("5 - Estatísticas")
    print("6 - Encerrar")


def executar_programa():
    sessoes = []

    while True:
        mostrar_menu()
        opcao = ler_inteiro("Escolha: ", 1, 6)

        if opcao == 1:
            cadastrar_sessao(sessoes)
        elif opcao == 2:
            listar_sessoes(sessoes)
        elif opcao == 3:
            buscar_sessao(sessoes)
        elif opcao == 4:
            ordenar_sessoes(sessoes)
        elif opcao == 5:
            mostrar_estatisticas(sessoes)
        else:
            print("\nPrograma encerrado. Obrigado por utilizar o LightWeek.")
            break


if __name__ == "__main__":
    try:
        executar_programa()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado pelo usuário.")
