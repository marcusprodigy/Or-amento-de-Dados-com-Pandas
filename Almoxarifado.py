# Importa as bibliotecas necessárias
import pyodbc, os, pandas as pd


# Função para consultar os dados do banco de dados
def ReqDataex(data, mod):
    pd.set_option("display.max_rows", None)
    # Carrega o banco de dados CSV para um dataframe Pandas
    df = pd.read_csv("almoxarifado.csv")

    # Verifica se o parâmetro `data` é um número
    if type(data) == int:
        # Consulta o produto pelo código de barras ou EAN
        if mod == 0:
            resultado = df[df["EAN"] == str(data)]
            desc = resultado["DESC"].values[0]
            qtd = resultado["QTD"].values[0]
            price = resultado["PRICE"].values[0]
            ean = resultado["EAN"].values[0]

            # Retorna um array com os dados do produto
            return [desc, qtd, price, ean]

        resultado = df[df["EAN"] == str(data)]
        desc = resultado["DESC"].values[0]
        qtd = resultado["QTD"].values[0]
        price = resultado["PRICE"].values[0]
        ean = resultado["EAN"].values[0]

        # Retorna um array com os dados do produto mais Numerador
        return [desc, 1, float(price), qtd, ean]

    # Consulta o produto pelo nome
    else:
        # Consulta os produtos que correspondem ao nome
        resultados = df[df["DESC"].str.contains(data, case=False, na=False)]
        desc = resultados["DESC"].tolist()
        qtd = resultados["QTD"].tolist()
        price = resultados["PRICE"].tolist()
        eans = resultados["EAN"].tolist()
        Lista = list(zip(desc, qtd, price, eans))
        if mod == 1:
            for indice, produto in enumerate(Lista):
                print(
                    f"ID. {indice}\n - {produto[0]}\nQTD. ESTOQUE: {produto[1]} VALOR DO PRODUTO: R$ {produto[2]}\n  Cod.{produto[3]}"
                )
                print(
                    "------------------------------------------------------------------------------------"
                )
            try:
                escolha = None
                escolha = int(input("Deseja Adicionar qual?\n"))
            except ValueError:
                print("Opção inválida.")

            if escolha == None:
                os.system("cls")
                return
            else:
                try:
                    qtd = int(input("Quantas Unidades?\n"))
                except ValueError:
                    print("Opção inválida.")

            return [
                Lista[escolha][0],
                qtd,
                float(Lista[escolha][2]),
                Lista[escolha][1],
                Lista[escolha][3],
            ]
        # Retorna uma lista com os produtos encontrados
        return list(zip(desc, qtd, price, eans))


# Função para consultar um produto por código
def ConsultaCod():
    mod = 0

    while True:
        print("________________________________________________")
        # Declara uma variável para armazenar o código do produto
        barcode = input(
            "Informe o Código do Produto ou 0 - Para retornar para o menu\n________________________________________________\n\n"
        )
        # Verifica se o código do produto é válido
        if barcode.isdigit():
            barcode = int(barcode)
        os.system("cls")

        if barcode == 0:
            os.system("cls")
            break

        else:
            os.system("cls")

            # Consulta os dados do produto
            produtos = ReqDataex(barcode, mod)
            if type(barcode) == str:
                print("____________PRODUTOS_____________________________")
                for produto in produtos:
                    print(
                        f"PRODUTO: {produto[0]}\nQTD. ESTOQUE: {produto[1]}\nVALOR DO PRODUTO: R$ {produto[2]}\nCod.{produto[3]}"
                    )
                    print(
                        "------------------------------------------------------------------------------------"
                    )
            else:
                os.system("cls")

                print(
                    f"PRODUTO: {produtos[0]}\n----------------------\nQTD. ESTOQUE: {produtos[1]}\nVALOR DO PRODUTO: R$ {produtos[2]}\nCod.{produtos[3]}"
                )

    main()


def Criarorcamento():
    lista = []
    mod = 1
    # Solicita ao usuário o código do produto
    while True:
        barcode = input("Informe o NOME ou Codigo de Barras \n")
        if barcode.isdigit():
            barcode = int(barcode)
        if barcode == 0:
            os.system("cls")
            break
        elif barcode == 1:
            print("imprimindo")
        else:
            produtos = ReqDataex(barcode, mod)
            if produtos == None:
                # Imprime os dados do produto

                os.system("cls")
                vt = 0
                print("ORÇAMENTO CLIENTE")
                print("---------------------------------------------")
                for produto in lista:
                    print(
                        f"{produto[0]}\nQTDE: {produto[1]} | VALOR UNTÁRIO R${produto[2]}\nCod.{produto[4]}"
                    )
                    print("---------------------------------------------")
                for produto in lista:
                    vt = vt + (produto[2] * produto[1])
                print(f"VALOR TOTAL: R$. {round(vt,1)}\n\n\n")
            else:
                os.system("cls")

                if len(lista) == 0:
                    lista.append(produtos)
                    os.system("cls")
                else:
                    produto_ja_na_lista = False
                    for i, item in enumerate(lista):
                        if item[0] == produtos[0]:  # Comparando o nome do produto
                            lista[i][1] = lista[i][1] + 1
                            produto_ja_na_lista = True

                    if not produto_ja_na_lista:
                        lista.append(produtos)
                # Imprime o orçamento

                vt = 0

                print("ORÇAMENTO CLIENTE")
                print("---------------------------------------------")
                for produto in lista:
                    print(
                        f"{produto[0]}\nQTDE: {produto[1]} | VALOR UNTÁRIO R${produto[2]}\nCod.{produto[4]}"
                    )
                    print("---------------------------------------------")
                for produto in lista:
                    vt = vt + (produto[2] * produto[1])
                print(f"VALOR TOTAL: R$. {round(vt,1)}\n\n\n")
    main()


def main():
    while True:
        print("_________ Consulta de preços _________")
        print("1 - Consultar Item por Código\n2 - Criar Orçamento")
        opcao = None
        try:
            opcao = int(input("Digite a opção: "))
        except ValueError:
            print("Opção inválida.")

        if opcao == 1:
            os.system("cls")
            ConsultaCod()
        elif opcao == 2:
            os.system("cls")
            Criarorcamento()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
