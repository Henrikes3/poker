import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import pyodbc
import random
import io
from collections import Counter

# Configuração da conexão com o SQL Server
server = 'DESKTOP-0CKCVE4'  # Substitua pelo nome do seu servidor
database = 'banco_de_dados'  # Substitua pelo nome do seu banco de dados
conn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Variável de controle para rastrear a etapa do sorteio
etapa_sorteio = 0

# Lista global para armazenar as referências das imagens
imagens_tk = []

# Variável global para rastrear as cartas já sorteadas
cartas_sorteadas_total = []

def valor_numerico_carta(carta):
    """Converte o valor da carta para um número."""
    valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
               '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return valores.get(carta[3], 0)  # Retorna 0 se o valor não for encontrado

def verificar_sequencia(cartas_sorteadas_total):
    # Extrair apenas os números das cartas sorteadas
    numeros = [int(carta[0]) for carta in cartas_sorteadas_total]
    
    # Remover duplicatas e ordenar os números
    numeros = sorted(set(numeros))
    
    # Verificar sequência de 5 números consecutivos
    for i in range(len(numeros) - 4):
        # Verifica se os próximos 4 números formam uma sequência
        if numeros[i+4] == numeros[i] + 4:
            return True, numeros[i:i+5]
    
    return False, None
    
def verificar_royal_flush(cartas_sorteadas_total):
    naipes = [carta[1] for carta in cartas_sorteadas_total]
    numeros = sorted(int(carta[0]) for carta in cartas_sorteadas_total)
    royal_flush_numeros = [10, 11, 12, 13, 1]
    
    # Verifica se há 5 cartas do mesmo naipe
    contador_naipes = Counter(naipes)
    for naipe, contador in contador_naipes.items():
        if contador >= 5:
            # Verifica se as cartas formam uma sequência Royal Flush
            cartas_do_naipe = [carta for carta in cartas_sorteadas_total if carta[1] == naipe]
            numeros_do_naipe = sorted(int(carta[0]) for carta in cartas_do_naipe)
            if all(numero in numeros_do_naipe for numero in royal_flush_numeros):
                return True, naipe
    return False, None

def verificar_straight_flush(cartas_sorteadas_total):
    # Extrair naipes e números das cartas
    naipes = [carta[1] for carta in cartas_sorteadas_total]
    numeros = [int(carta[0]) for carta in cartas_sorteadas_total]
    
    # Verificar se há 5 cartas do mesmo naipe
    contador_naipes = Counter(naipes)
    for naipe, contador in contador_naipes.items():
        if contador >= 5:
            # Filtrar cartas do mesmo naipe
            cartas_do_naipe = [carta for carta in cartas_sorteadas_total if carta[1] == naipe]
            numeros_do_naipe = sorted(int(carta[0]) for carta in cartas_do_naipe)
            
            # Verificar se há uma sequência de 5 cartas
            for i in range(len(numeros_do_naipe) - 4):
                if numeros_do_naipe[i+4] == numeros_do_naipe[i] + 4:
                    return True, naipe  # Retorna True e o naipe do Straight Flush
    
    # Se não encontrar um Straight Flush
    return False, None

def verificar_combinacoes():
    global etapa_sorteio, cartas_sorteadas_total
    contador_naipes = Counter(carta[1] for carta in cartas_sorteadas_total)
    contador_numeros = Counter(carta[0] for carta in cartas_sorteadas_total)
    nomes = (carta[3] for carta in cartas_sorteadas_total)
    
    tem_royal_flush, naipe = verificar_royal_flush(cartas_sorteadas_total)
    if tem_royal_flush:
        messagebox.showinfo("Royal Flush", f"Royal Flush")
        reiniciar_jogo()
        return
    
    tem_straight_flush, naipe = verificar_straight_flush(cartas_sorteadas_total)
    if tem_straight_flush:
        messagebox.showinfo("Straight Flush", "Straight Flush!")
        reiniciar_jogo()
        return
    for quadra, contadornu in contador_numeros.items():
        if contadornu == 4:
            messagebox.showinfo("Quadra","Quadra")
            reiniciar_jogo()
            return
    tem_trio = False
    tem_par = False
    for fullhouse, contadornu in contador_numeros.items():
        if contadornu == 3:
            tem_trio = True
        if contadornu == 2:
            tem_par = True
        if tem_trio and tem_par:
            messagebox.showinfo("Full House","Full House")
            reiniciar_jogo()
            return
    for flush, contadorna in contador_naipes.items():
        if contadorna >= 5:
            messagebox.showinfo("Flush","Flush")
            reiniciar_jogo()
            return
    tem_sequencia, sequencia = verificar_sequencia(cartas_sorteadas_total)
    if tem_sequencia:
        messagebox.showinfo("Sequencia","Sequencia")
        reiniciar_jogo()
        return
    for trio, contadornu in contador_numeros.items():
        if contadornu == 3:
            messagebox.showinfo("Trio", "Trio")
            reiniciar_jogo()
            return
    pares = 0
    for doispares, contadornu in contador_numeros.items():
        if contadornu == 2:
            pares += 1
        if pares >= 2:
            messagebox.showinfo("Dois Pares", "Dois Pares")
            reiniciar_jogo()
            return
    for umpar, contadornu in contador_numeros.items():
        if contadornu == 2:
            messagebox.showinfo("Um Par", "Um Par")
            reiniciar_jogo()
            return
    else:
        carta_mais_alta = max(cartas_sorteadas_total[:2], key=lambda carta: valor_numerico_carta(carta))
        valor_carta_mais_alta = carta_mais_alta[3]
        naipe_carta_mais_alta = carta_mais_alta[1]
        messagebox.showinfo("Maior Carta",f"{valor_carta_mais_alta} de {naipe_carta_mais_alta}")
        reiniciar_jogo()
        return
def reiniciar_jogo():
    global etapa_sorteio, cartas_sorteadas_total
    etapa_sorteio = 0
    cartas_sorteadas_total = []
    for widget in frame_cartas_mesa.winfo_children():
        widget.destroy()
    for widget in frame_cartas_mao.winfo_children():
        widget.destroy()

def sortear_cartas():
    global etapa_sorteio, imagens_tk, cartas_sorteadas_total  # Referenciar as variáveis globais
    
    # Limpar a lista de referências das imagens
    imagens_tk.clear()
    
    # Conectar ao banco e buscar as imagens
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT NUMERO, NAIPE, IMAGEM, NOME FROM dbo.BARALHO")
    cartas = cursor.fetchall()
    conn.close()
    
    # Remover as cartas já sorteadas da lista de cartas disponíveis
    cartas_disponiveis = [carta for carta in cartas if carta not in cartas_sorteadas_total]
    
    # Se não houver cartas suficientes disponíveis, reinicia o jogo
    if len(cartas_disponiveis) == 0:
        etapa_sorteio = 0
        cartas_sorteadas_total = []  # Reiniciar as cartas sorteadas
        return
    
    # Definir quantas cartas sortear com base na etapa atual
    if etapa_sorteio == 0:
        # Limpar a mesa
        for widget in frame_cartas_mesa.winfo_children():
            widget.destroy()
        for widget in frame_cartas_mao.winfo_children():
            widget.destroy()

        # Sortear 2 cartas para a mão
        cartas_sorteadas = random.sample(cartas_disponiveis, 2)
        frame_alvo = frame_cartas_mao

    elif etapa_sorteio == 1:
        # Sortear 3 cartas para a mesa
        cartas_sorteadas = random.sample(cartas_disponiveis, 3)
        frame_alvo = frame_cartas_mesa
    elif etapa_sorteio == 2:
        # Sortear mais 1 carta para a mesa
        cartas_sorteadas = random.sample(cartas_disponiveis, 1)
        frame_alvo = frame_cartas_mesa
    elif etapa_sorteio == 3:
        # Sortear mais 1 carta para a mesa
        cartas_sorteadas = random.sample(cartas_disponiveis, 1)
        frame_alvo = frame_cartas_mesa
    else:
         # Verifica as combinações
        verificar_combinacoes()
        return

    # Adicionar as cartas sorteadas à lista global
    cartas_sorteadas_total.extend(cartas_sorteadas)
    
    # Exibir as cartas sorteadas
    for carta in cartas_sorteadas:
        # Converter o binário em imagem
        imagem_bytes = carta[2]
        imagem = Image.open(io.BytesIO(imagem_bytes))
        imagem = imagem.resize((100, 150))  # Redimensionar para caber na tela
        imagem_tk = ImageTk.PhotoImage(imagem)
        
        # Armazenar a referência da imagem na lista global
        imagens_tk.append(imagem_tk)
        
        # Exibir a imagem na tela
        label = Label(frame_alvo, image=imagem_tk)
        label.image = imagem_tk  # Necessário para manter a referência
        label.pack(side=tk.LEFT, padx=5)
    
    # Avançar para a próxima etapa
    etapa_sorteio += 1


# Configuração da interface gráfica
root = tk.Tk()
root.title('Poker')
root.geometry('700x400')

# Frame para exibir as cartas da mesa
frame_cartas_mesa = tk.Frame(root)
frame_cartas_mesa.pack(pady=10)

# Frame para exibir as cartas da mão
frame_cartas_mao = tk.Frame(root)
frame_cartas_mao.pack(pady=10)

# Botão para sortear cartas
btn_sortear = tk.Button(root, text="Sortear Cartas", command=sortear_cartas)
btn_sortear.pack(side=tk.BOTTOM, anchor='s',pady=10)

# Executar a interface
root.mainloop()
