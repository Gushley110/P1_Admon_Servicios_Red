import os.path, threading, SNMPAdmin
from os import remove
from reportlab.pdfgen import canvas

def addAgent():
    archivo = open('agentes.txt', 'ta')
    direccion = str(input("Introduce IP: "))
    version = str(input("Introduce SNMP version: "))
    comunidad = str(input("Introduce community: "))
    puerto = str(input("Introduce interface: "))
    linea = str(direccion +" "+ version +" "+ comunidad +" "+ puerto +"\n" )
    archivo.write(linea)
    archivo.close()
    SNMPAdmin.createRRD(direccion)

    hilo = threading.Thread(target=SNMPAdmin.updateRRD, args=(direccion, version, comunidad, puerto))
    hilo.start()
    
    print("Agent added\n")

def deleteAgent():
    agente = str(input("Introduce IP: "))
    archivo = open('agentes.txt', 'r+')
    texto = archivo.read()
    lista = texto.split("\n")
    texto = ""
    for aux in lista:
        if aux.find(agente):
            texto += aux + "\n"
        else:
            texto += ""
    archivo.seek(0)
    archivo.truncate()
    archivo.write(texto)
    archivo.close()

    print("Agent deleted\n")
    remove(agente + ".rrd")
    remove(agente + ".xml")
    if os.path.isfile("reporte-" + agente + ".pdf"):
        remove("reporte-" + agente + ".pdf")
    if os.path.isfile(agente + "_1.png"):
        remove(agente + "_1.png")
    if os.path.isfile(agente + "_2.png"):
        remove(agente + "_2.png")
    if os.path.isfile(agente + "_3.png"):
        remove(agente + "_3.png")
    if os.path.isfile(agente + "_4.png"):
        remove(agente + "_4.png")
    if os.path.isfile(agente + "_5.png"):
        remove(agente + "_5.png")

def generateReport():
    direccion = str(input("Introduce host: "))
    minutos = str(input("Introduce report time: "))
    SNMPAdmin.graphRRD(minutos, direccion)
    SNMPAdmin.createPDF(direccion)
    print("Report created\n")

def showAgents():
    archivo = open('agentes.txt', 'r')
    texto = archivo.read()
    print(texto + "\n")

def agentResume():
    archivo = open('agentes.txt', 'r')
    texto = archivo.read()
    lista = texto.split("\n")
    dispositivos = 0

    for aux in lista:
        agente = aux.split(" ")
        if agente[0] != "":
            dispositivos = dispositivos + 1

            print("\n Agent: " + agente[0])
            estatus_agente = str(SNMPAdmin.snmpGet(agente[2], agente[0], '1.3.6.1.2.1.2.2.1.7.' +agente[3]))
            print("Agent status: " + str(estatus_agente))
            if estatus_agente != 0:
                print("\t Up")
            else:
                print("\t Down")

            num_puertos = str(SNMPAdmin.snmpGet(agente[2], agente[0], '1.3.6.1.2.1.2.1.0'))
            print("\tAgent interfaces: " + num_puertos)

    print("\nTotal devices: " + str(dispositivos) + "\n")
    
salir = False
while not salir:
    print("1.- Add agent")
    print("2.- Delete agent")
    print("3.- Create report")
    print("4.- Show agents")
    print("5.- Agents resume")
    opcion = 0
    opcion = int(input("Choose an option: "))
    if opcion == 1:
        addAgent()
    elif opcion == 2:
        deleteAgent()
    elif opcion == 3:
        generateReport()
    elif opcion == 4:
        showAgents()
    elif opcion == 5:
        agentResume()
    else:
        print("Choose valid option\n")