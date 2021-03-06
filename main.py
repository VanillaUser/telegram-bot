import logging
import data

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


aeropuertoNombre = ""
ciudad = ""
asientos = 0
precio = 0
iatac = ""
tickets = False
buy_off = True

def start(update, context):
    update.message.reply_text("""Los siguientes comandos te ayudaran con lo que necesites:
    /listar Lista los vuelos y precios de todas las aerolineas a disposicion
    /buscar Permite buscar vuelos de aeropuertos, vuelos por ciudades, vuelos por paises
    /comprar_t Comprar un ticket de ida.
    /comprar_rt Comprar un ticket de ida y regreso
    Siempre puedes usar el comando /start para recordar los diferentes comandos
    Escribelo directamente en el chat y encuentra resultados.
    """)

def listar(update, context):
    for iata in data.database:
        arr = []
        for vuelo in iata["vuelos"]:
            nombre_aero = iata["nombre"]
            ciudad = vuelo["ciudad"]
            precio = vuelo["precio"]
            arr.append(f"{ciudad}          {precio}\n")
        update.message.reply_text(f"{nombre_aero}\n" + "Ciudad          Precio\n" + "".join(map(str, arr)))

def search(update, context):
    update.message.reply_text("""Deseas buscar por:
    Codigo iata
    Nombre de aeropuerto
    Ciudad
    Pais
    Escribelo directamente en el chat y encuentra resultados.
    """)

def do_everything(update, context):
    global aeropuertoNombre
    global ciudad
    global asientos
    global precio
    global iatac
    global tickets
    global buy_off
    msg = update.message.text.lower()
    for iata in data.database:

        if (buy_off):
            for vuelo in iata["vuelos"]:

                if (msg == vuelo["ciudad"].lower()):
                    c = vuelo["ciudad"]
                    p = vuelo["precio"]
                    update.message.reply_text(f"El vuelo hacia {c} cuesta {p}")

                elif (msg == vuelo["pais"].lower()):
                    imp_pais(update, iata)

            if (msg == iata["iata"].lower()):
                imp(update,iata)

            elif (msg == iata["nombre"].lower()):
                imp(update,iata)

        else :
            if (msg.isdigit() and ciudad and iatac.lower() == iata["iata"].lower()):
                asientos = int(msg)
                if (tickets == False):
                    update.message.reply_text("Vuelo de ida\n" + f"{aeropuertoNombre}\nCiudad: {ciudad}\nAsientos: {asientos}\nPrecio total: {precio * asientos}")
                    buy_off = True
                else:
                    update.message.reply_text("Vuelo de ida y regreso\n" + f"{aeropuertoNombre}\nCiudad: {ciudad}\nAsientos: {asientos}\nPrecio total: {precio * asientos * 2}")
                    buy_off = True
                    tickets = False    
            elif (msg.find(iata["iata"].lower()) == 0):
                aeropuertoNombre = iata["nombre"]
                iatac = iata["iata"]
                update.message.reply_text("Escribe el nombre de la ciudad")
                imp(update, iata)
            elif (aeropuertoNombre):
                for vuelo in iata["vuelos"]:
                    if (msg.lower().find(vuelo["ciudad"].lower()) == 0):
                        ciudad = vuelo["ciudad"]
                        precio = vuelo["precio"]
                        update.message.reply_text("¿Cuantos asientos quieres?: \nEscribe el numero de asientos\n")

def buy_ticket(update, context):
    global buy_off
    buy_off = False
    b_t(update, context)

def buyRt_ticket(update, context):
    global tickets
    global buy_off
    tickets = True
    buy_off = False
    b_t(update, context)

def b_t(update, context):
    update.message.reply_text("Escoge el Aeropuerto de origen\n Escribe el codigo iata")
    arr = []
    for iata in data.database:
        codigo = iata["iata"]
        count = 1
        arr.append(f"· {codigo}\n")
        count = count + 1
    update.message.reply_text("".join(map(str, arr)))
    

def imp(update,iata):
    arr = []
    for vuelo in iata["vuelos"]:
        ciudad = vuelo["ciudad"]
        precio = str(vuelo["precio"])
        space = (45 - len(ciudad))
        arr.append(f"{ciudad.ljust(space, '.')}{precio.rjust(10)}\n")
    update.message.reply_text(f"Ciudad  Precio\n" + "".join(map(str, arr)))
    print(f"Ciudad  Precio\n" + "".join(map(str, arr)))

def imp_pais(update, iata):
    arr = []
    for vuelo in iata["vuelos"]:
        if (update.message.text.lower().find(vuelo["pais"].lower()) == 0):
            nombre_aero = iata["nombre"]
            ciudad = vuelo["ciudad"]
            precio = vuelo["precio"]
            pais  = vuelo["pais"]
            arr.append(f"{ciudad}          {precio}\n")
    update.message.reply_text("%s\n" % (nombre_aero) + "Viaje a: %s\n" % (pais) + "Ciudad          Precio\n" + "".join(map(str, arr)))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    updater = Updater("1650626119:AAFGkMENmoTL0nisaMDa8blSPHnAC7P2i0M", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("listar", listar))
    dp.add_handler(CommandHandler("buscar", search))
    dp.add_handler(CommandHandler("comprar_t", buy_ticket))
    dp.add_handler(CommandHandler("comprar_rt", buyRt_ticket))
    dp.add_handler(MessageHandler(Filters.text, do_everything))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

