import logging
import data
import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

aeropuerto = data.database[0]

aeropuertoNombre = ""
ciudad = ""
asientos = 0
precio = 0
iatac = ""

def start(update, context):
    update.message.reply_text('Hi')

def help(update, context):
    update.message.reply_text('Help!')

def listar(update, context):
    arr = []
    for vuelo in aeropuerto["vuelos"]:
        print(vuelo)
        ciudad = vuelo["ciudad"]
        precio = vuelo["precio"]
        arr.append(f"{ciudad}          {precio}\n")
    update.message.reply_text("Ciudad          Precio\n" + "".join(map(str, arr)))

def search(update, context):
    update.message.reply_text("""Deseas buscar por:
    Codigo iata
    Nombre de aeropuerto
    Ciudad
    Pais
    Escribelo directamente en el chat y encuentra resultados.
    """)
    # searhAll(update, context)
    # if (update.message. == "1"):
    #     update.message.reply_text("Escriba el codigo IATA")
    #     for iata in data.database:
    #         if (update.message.text == iata["iata"]):
    #             arr = []
    #             for vuelo in aeropuerto["vuelos"]:
    #                 print(vuelo)
    #                 ciudad = vuelo["ciudad"]
    #                 precio = vuelo["precio"]
    #                 arr.append(f"{ciudad}          {precio}\n")
    #             update.message.reply_text("Ciudad          Precio\n" + "".join(map(str, arr)))

    # elif (update.message.text == "2"):
    #     update.message.reply_text("Escriba el nombre del aeropuerto")

    # elif (update.message.text == "3"):
    #     update.message.reply_text("Escriba la ciudad")

    # elif (update.message.text == "4"):
    #     update.message.reply_text("Escriba el pais")

def do_everything(update, context):
    global aeropuertoNombre
    global ciudad
    global asientos
    global precio
    global iatac
    message = update.message.text.lower().split("/")
    msg = message[-1]
    # print(msg)

    # print(message)
    for iata in data.database:
        # print(iata["iata"])

        # print(update.message.text.upper())
        # print(update.message.text.upper().find(iata["iata"]))

        if (len(message) == 1):
            for vuelo in iata["vuelos"]:

                if (msg == vuelo["ciudad"].lower()):
                    c = vuelo["ciudad"]
                    p = vuelo["precio"]
                    update.message.reply_text(f"El vuelo hacea {c} cuesta {p}")

                elif (msg == vuelo["pais"].lower()):
                    imp2(update, iata)

            if (msg == iata["iata"].lower()):
                imp(update, iata)

            elif (msg == iata["nombre"].lower()):
                imp(update, iata)

        else :
            # print(msg)
            # number = re.findall('[0-9]+', message)
            # num = "".join(map(str, number))
            # print(number)
            # print(num)
            # print(message)
            # print(msg.isdigit())
            # print(type(int(message)) is int)
            print(ciudad)
            print(iatac)
            if (msg.isdigit() and ciudad and iatac.lower() == iata["iata"].lower()):
                asientos = int(msg)
                # print(asientos)
                update.message.reply_text(f"{aeropuertoNombre}\nciudad: {ciudad}\nasientos: {asientos}\nprecio total: {precio * asientos}")
            elif (msg.find(iata["iata"].lower()) == 0):
                aeropuertoNombre = iata["nombre"]
                iatac = iata["iata"]
                print(iatac)
                update.message.reply_text("Escoge la ciudad\n Escribe \"/ + nombre de la ciudad\"")
                imp(update, iata)
            elif (aeropuertoNombre):
                for vuelo in iata["vuelos"]:
                    if (msg.lower().find(vuelo["ciudad"].lower()) == 0):
                        ciudad = vuelo["ciudad"]
                        precio = vuelo["precio"]
                        update.message.reply_text("¿Cuantos asientos quieres?: \nEscribe \"/ + el numero de asientos\n")


def buy_ticket(update, context):
    update.message.reply_text("Escoge el Aeropuerto de origen\n Escribe \"/ + codigo iata\" ")
    arr = []
    for iata in data.database:
        codigo = iata["iata"]
        count = 1
        arr.append(f"· {codigo}\n")
        count = count + 1
    update.message.reply_text("".join(map(str, arr)))


def buyRt_ticket(update, context):
    update.message.reply_text("Escoge el A ")

# def do_everything(update, context):
#     for iata in data.database:
#         message = update.message.text.lower().split("/")
#         print(message[1])
#         print(iata["iata"].lower())
#         print(message[1].find(iata["iata"].lower()) == 0)

#         if(message[1].find(iata["iata"].lower()) == 0):
#             update.message.reply_text("Escoge la ciudad\n Escribe \"/ + nombre de la ciudad\"")
#             # imp(update, iata)

def imp(update, iata):
    arr = []
    for vuelo in iata["vuelos"]:
        ciudad = vuelo["ciudad"]
        precio = vuelo["precio"]
        arr.append(f"{ciudad}          {precio}\n")
    update.message.reply_text("Ciudad          Precio\n" + "".join(map(str, arr)))

def imp2(update, iata):
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
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("listar", listar))
    dp.add_handler(CommandHandler("buscar", search))
    dp.add_handler(CommandHandler("buy", buy_ticket))
    dp.add_handler(MessageHandler(Filters.text, do_everything))
    # dp.add_handler(MessageHandler(Filters.text, searchAll))


    # dp.add_handler(CommandHandler("buscar " + Filters.text, search))

    # dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

