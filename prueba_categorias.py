from tickets.categorias import CategoriaTicket, recorrer_categorias

if __name__ == "__main__":
    hardware = CategoriaTicket("Hardware")
    hardware.agregar_subcategoria(CategoriaTicket("Impresoras"))
    hardware.agregar_subcategoria(CategoriaTicket("Monitores"))

    software = CategoriaTicket("Software")
    software.agregar_subcategoria(CategoriaTicket("Sistema operativo"))
    software.agregar_subcategoria(CategoriaTicket("Aplicaciones"))

    redes = CategoriaTicket("Redes")
    redes.agregar_subcategoria(CategoriaTicket("Conexión Wi-Fi"))
    redes.agregar_subcategoria(CategoriaTicket("VPN"))

    raiz = CategoriaTicket("Categorías de Soporte")
    raiz.agregar_subcategoria(hardware)
    raiz.agregar_subcategoria(software)
    raiz.agregar_subcategoria(redes)

    recorrer_categorias(raiz)
