import json
import random

players = {'player1':'Tonyn Stallone','player2':'Arnaldor Shautseneguer'}
botones = {'A':'Izquierda', 'D':'Derecha', 'W':'Arriba', 'S':'Abajo', 'P':'Puño', 'K':'Patada'}

comentarios = ["", "ATANGANA!! ", "esto es increible! ", "POR POQUIIIIIITO!!! ", "Toasty!!!"]

movimientos = {'player1':{'D':'avanza','A':'retrocede','W':'salta','S':'agacha'}, 'player2':{'A':'avanza','D':'retrocede','W':'salta','S':'agacha'}}

combinaciones = {
    'player1':[
        {'combinacion':'DSD','golpe':'P','puntos':3,'nombre':'Taladoken'},
        {'combinacion':'SD','golpe':'K','puntos':2,'nombre':'Remuyuken'},
        {'combinacion':'','golpe':'P','puntos':1,'nombre':'Puño'},
        {'combinacion':'','golpe':'K','puntos':1,'nombre':'Patada'}],
    'player2':[
        {'combinacion':'SA','golpe':'K','puntos':3,'nombre':'Remuyuken'},
        {'combinacion':'ASA','golpe':'P','puntos':2,'nombre':'Taladoken'},
        {'combinacion':'','golpe':'P','puntos':1,'nombre':'Puño'},
        {'combinacion':'','golpe':'P','puntos':1,'nombre':'Patada'}]
    }

jugadas_demo = {"player1":{"movimientos":["D","DSD","S","DSD","SD"],"golpes":["K","P","","K","P"]},"player2": {"movimientos":["SA","SA","SA","ASA","SA"],"golpes":["K","","K","P","P"]}} 

def validarJugadas(_jugadas):
    if len(_jugadas) == 0:
        return False, 'Json vacio'
    try:
        jugadas = json.loads(_jugadas)
        
        if 'player1' not in jugadas or 'player2' not in jugadas:
            return False, 'No define jugadores'
        if 'movimientos' not in jugadas['player1'] or  'movimientos' not in jugadas['player2']:
            return False, 'No entrega lista de movimientos'
        if 'golpes' not in jugadas['player1'] or  'golpes' not in jugadas['player2']:
            return False, 'No entrega lista de golpes'
        
    except Exception as e:
        print(e)
        return False, "No es un formato permitido"
    return True, 'Ok'

def damageMovimiento(_player="player1", _movimiento='', _golpe=''):
    damage = 1
    if _golpe == '':
        return 0
    
    if len(_movimiento) <= 1:
        return 1

    for c in combinaciones[_player]:
        if _movimiento in c['combinacion'] or c['combinacion'].endswith(_movimiento):
            damage = c['puntos']
            break
    return damage

def crearTexto(_player, _movimiento, _golpe):
    texto = ''
    nombrePlayer = players[_player].split(' ')[0]
    boton = botones[_golpe] if len(_golpe) > 0 or _golpe != '' else ''
    comentarista = comentarios[random.randint(0,len(comentarios)-1)]
    
    if len(_movimiento) == 0:
        texto += f' conecta {boton}'
        if _golpe == "P" and comentarista == 'Toasty!!!':
            texto += comentarista
    
    elif len(_movimiento) == 1:
        texto += ' {}'.format(movimientos[_player][_movimiento.upper()])
        if boton != '':
            texto += f' y conecta {boton}'
            if _golpe == "P" and _movimiento.upper() == 'S' and comentarista == 'Toasty!!!':
                texto += 'TOASTIIII!!!'
            
    elif _golpe == '':
        texto = f'se mueve'
    else:
        for c in combinaciones[_player]:
            if _movimiento.upper() in c['combinacion'] or c['combinacion'].endswith(_movimiento) and  c['golpe'] == _golpe:
                texto += f' {comentarista} conecta un {c["nombre"]}'
                break
    if texto == '' and len(_movimiento) > 0:
        lastStr = _movimiento.upper()[-1]
        texto = "{0}".format(movimientos[_player][lastStr])
    
    return f"{nombrePlayer} {texto}" 
    
def cantidadCombinaciones(_movimiento='', _golpe=''):
    return len(_movimiento) + len(_golpe)

def cantidadMovimientos(_movimiento=''):
    return len(_movimiento)

def cantidadGolpes(_golpe=''):
    return len(_golpe)


def inciaPlayer1(jugadas):
    combinacionePlayer1 = cantidadCombinaciones(jugadas['player1']['movimientos'][0], jugadas['player1']['golpes'][0])
    combinacionePlayer2 = cantidadCombinaciones(jugadas['player2']['movimientos'][0], jugadas['player2']['golpes'][0])
    
    movimientosPlayer1 = cantidadMovimientos(jugadas['player1']['movimientos'][0])
    movimientosPlayer2 = cantidadMovimientos(jugadas['player2']['movimientos'][0])
    
    golpesPlayer1 = cantidadGolpes(jugadas['player1']['golpes'][0])
    golpesPlayer2 = cantidadGolpes(jugadas['player2']['golpes'][0])
    
    if combinacionePlayer1 == combinacionePlayer2:
        if movimientosPlayer1 == movimientosPlayer2:
            if golpesPlayer1 > golpesPlayer2:
                return False
            
        elif movimientosPlayer1 > movimientosPlayer2:
            return False
        
    elif combinacionePlayer1 > combinacionePlayer2:
        return False
    
    return True

def turno (_player, _movimiento, _golpe, _vidaRival):
    print(crearTexto(_player,_movimiento, _golpe))
    
    damagePlayer = damageMovimiento(_player, _movimiento, _golpe)
    
    vidaRival = _vidaRival - damagePlayer
    return vidaRival

if __name__ == "__main__":
    jugadas = {}
    es_valido, mensaje = False, ''
    while(True):
        jugadas = input ("Inserta archivos movimientos:")
        if len(jugadas) > 0:
            es_valido, mensaje = validarJugadas (jugadas)
            if (es_valido):
                jugadas = json.loads(jugadas)
                break
        else:
            mensaje = 'Debe ingresar Json con los movimientos'
        print(f"Error: {mensaje}")
    
    
    if es_valido:
        finishIm = False
        vidaPlayer1 = 6
        vidaPlayer2 = 6
        
        player1Name = players['player1'].split(' ')[0]
        player2Name = players['player2'].split(' ')[0]
        
        inicia1 = inciaPlayer1(jugadas)

        print('¡¡¡Inicia el torneo Kombat!!! Atangana!!! golpea primero...', player1Name if inicia1 else  player2Name)
        
        cantMovimientosTotalPorJugador1 = len(jugadas['player1']['movimientos'])
        cantMovimientosTotalPorJugador2 = len(jugadas['player2']['movimientos'])
        cantMovimientosTotalPorJugador = (cantMovimientosTotalPorJugador1 if cantMovimientosTotalPorJugador1 > cantMovimientosTotalPorJugador2 else cantMovimientosTotalPorJugador2)
        
        for x in range(0,cantMovimientosTotalPorJugador):

            if inicia1:
                if cantMovimientosTotalPorJugador1 > x:
                    vidaPlayer2 = turno("player1", jugadas['player1']['movimientos'][x], jugadas['player1']['golpes'][x], vidaPlayer2)
                    if vidaPlayer2 <= 0:
                        print (f'{player1Name} Gana la pelea y aun le queda {vidaPlayer1} de energia')
                        finishIm = True
                        break
                
                if cantMovimientosTotalPorJugador2 > x:
                    vidaPlayer1 = turno("player2", jugadas['player2']['movimientos'][x], jugadas['player2']['golpes'][x], vidaPlayer1)
                    if vidaPlayer1 <= 0:
                        print (f'{player2Name} Gana la pelea y aun le queda {vidaPlayer2} de energia')
                        finishIm = True
                        break
                    
            else:
                if cantMovimientosTotalPorJugador2 > x:
                    vidaPlayer1 = turno("player2", jugadas['player2']['movimientos'][x], jugadas['player2']['golpes'][x], vidaPlayer1)
                    if vidaPlayer1 <= 0:
                        print (f'{player2Name} Gana la pelea y aun le queda {vidaPlayer2} de energia')
                        finishIm = True
                        break
                if cantMovimientosTotalPorJugador1 > x:
                    vidaPlayer2 = turno("player1", jugadas['player1']['movimientos'][x], jugadas['player1']['golpes'][x], vidaPlayer2)
                    if vidaPlayer2 <= 0:
                        print (f'{player1Name} Gana la pelea y aun le queda {vidaPlayer1} de energia')
                        finishIm = True
                        break
        
        if finishIm == False:
            if vidaPlayer1 == vidaPlayer2:
                print (f'Que emoción, esto ha sido un empate entre {player1Name} y {player1Name}, ambos con {vidaPlayer1} de energia')
            elif vidaPlayer1 > vidaPlayer2:
                print (f'Que emoción, se acabaron los turnos y {player1Name} gana la pelea y aun le queda {vidaPlayer1} de energia')
            else:
                print (f'Que emoción, se acabaron los turnos y {player2Name} gana la pelea y aun le queda {vidaPlayer2} de energia')
                
