import random

while True:
    cartas = ['A♣', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣',
          'A♦', '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦',
          'A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥',
          'A♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠'
          ]

    cartas_npc = random.sample(cartas, 2)
    for carta in cartas_npc:
        cartas.remove(carta)
    cartas_jogador = random.sample(cartas, 2)
    for carta in cartas_jogador:
        cartas.remove(carta)
    cartas_mesa1 = random.sample(cartas, 3)
    for carta in cartas_mesa1:
        cartas.remove(carta)
    cartas_mesa2 = random.sample(cartas, 1)
    for carta in cartas_mesa2:
        cartas.remove(carta)
    cartas_mesa3 = random.sample(cartas, 1)

    print('Suas cartas: ',cartas_jogador)

    jogar = input('Quer jogar?(s/n)')

    if jogar == 's':
        print('Mesa: ',cartas_mesa1)
        print('Suas cartas: ', cartas_jogador)
    elif jogar == 'n':
        print('Mesa: ',cartas_mesa1)
        print('Mesa: ', cartas_mesa1, cartas_mesa2)
        print('Mesa: ', cartas_mesa1, cartas_mesa2, cartas_mesa3)
        print('Cartas adversário: ', cartas_npc)
        break

    continuar = input('Quer continuar?(s/n)')

    if continuar == 's':
        print('Mesa: ',cartas_mesa1, cartas_mesa2)
        print('Suas cartas: ', cartas_jogador)
    elif continuar == 'n':
        print('Mesa: ', cartas_mesa1, cartas_mesa2)
        print('Mesa: ', cartas_mesa1, cartas_mesa2, cartas_mesa3)
        print('Cartas adversário: ', cartas_npc)
        break
    continuar = input('Quer continuar?(s/n)')

    if continuar == 's':
        print('Mesa: ',cartas_mesa1, cartas_mesa2, cartas_mesa3)
        print('Suas cartas: ', cartas_jogador)
        print('Cartas adversario: ', cartas_npc)
        break
    elif continuar == 'n':
        print('Mesa: ', cartas_mesa1, cartas_mesa2, cartas_mesa3)
        print('Cartas adversário: ', cartas_npc)
        break
