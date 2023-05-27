import csv

def nutrition(file_path):
    kelompok_usia = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            kelompok_usia.append(row)
    
    for i in range(len(kelompok_usia)):
        nomor       = str(i + 1)
        kelompok    = kelompok_usia[i][0]
        print(nomor + ". " + kelompok)

    kelompok = int(input("Pilih kelompok usia: "))

    kebutuhan_nutrisi = {
        1: 2000, 2: 2400, 3: 2650, 4: 2650, 5: 2550, 6: 2150, 7: 1800,
        8: 1600, 9: 1900, 10: 2050, 11: 2100, 12: 2250, 13: 2150,
        14: 1800, 15: 1550, 16: 1400
    }.get(kelompok, None)

    if kebutuhan_nutrisi is None:
        print("Kelompok usia yang anda masukkan tidak ada. Coba ulangi!") 

    return kebutuhan_nutrisi


class Node:
    def __init__(self, level, energi_makanan, harga_makanan, menu_makanan):
        self.level          = level
        self.energi_makanan = energi_makanan
        self.harga_makanan  = harga_makanan
        self.menu_makanan   = menu_makanan


def cost(simpul, menu_makanan_terurut, uang_tersedia):
    bound        = simpul.energi_makanan
    total_harga  = simpul.harga_makanan
    level        = simpul.level

    while (level < len(menu_makanan_terurut)) and (total_harga + menu_makanan_terurut[level][1] <= uang_tersedia):
        level        += 1
        total_harga  += menu_makanan_terurut[level][1]
        bound        += menu_makanan_terurut[level][2]
    
    if level < len(menu_makanan_terurut):
        bound        += (uang_tersedia - total_harga) * (menu_makanan_terurut[level][2]/menu_makanan_terurut[level][1])
    return bound


def nutrition_measurement(menu_makanan, uang_tersedia):
    # menghitung densitas suatu makanan
    def rasio(item):
        return item[2]/item[1]

    # mengurutkan menu makanan berdasarkan densitas tertinggi ke terendah
    for i in range(len(menu_makanan)):
        maksimum_density = i
        for j in range(i+1, len(menu_makanan)):
            if rasio(menu_makanan[j]) > rasio(menu_makanan[maksimum_density]):
                maksimum_density = j
        temp                            = menu_makanan[i]
        menu_makanan[i]                 = menu_makanan[maksimum_density]
        menu_makanan[maksimum_density]  = temp

    queue                = []
    perolehan_nutrisi    = 0
    menu_makanan_terurut = menu_makanan

    # membuat simpul akar pada pohon ruang status
    simpul_akar          = Node(level=0, energi_makanan=0, harga_makanan=0, menu_makanan=[])
    queue.append(simpul_akar)

    # algoritma branch and bound
    while queue:
        simpul = queue.pop(0)
        if simpul.level == len(menu_makanan) - 1:
            continue

        # membuat simpul anak di cabang kiri yang menyatakan makanan saat ini dipilih (Xi=1)
        simpul_anak = Node(level = simpul.level + 1,
            energi_makanan  = simpul.energi_makanan + menu_makanan_terurut[simpul.level][2],
            harga_makanan   = simpul.harga_makanan  + menu_makanan_terurut[simpul.level][1],
            menu_makanan    = simpul.menu_makanan   + [menu_makanan_terurut[simpul.level][0]])

        # jika simpul anak masih memenuhi uang yang tersedia
        if simpul_anak.harga_makanan <= uang_tersedia:
            if simpul_anak.energi_makanan > perolehan_nutrisi:
                perolehan_nutrisi      = simpul_anak.energi_makanan
                menu_anjuran           = simpul_anak.menu_makanan
            queue.append(simpul_anak)

        # membuat simpul anak di cabang kanan yang menyatakan makanan saat ini tidak dipilih (Xi=0)
        simpul_anak = Node(level = simpul.level + 1,
            energi_makanan  = simpul.energi_makanan,
            harga_makanan   = simpul.harga_makanan,
            menu_makanan    = simpul.menu_makanan)

        # menghitung cost simpul
        bound = cost(simpul_anak, menu_makanan_terurut, uang_tersedia)

        # jika simpul masih mungkin menghasilkan nutrisi lebih besar daripada perolehan_nutrisi
        if bound > perolehan_nutrisi:
            queue.append(simpul_anak)

    return perolehan_nutrisi, menu_anjuran





def mainProgram():
    kebutuhan_nutrisi               = nutrition("kelompok-usia.csv")
    menu_makanan                    = [("Sup Ikan - Warung Makan Pidade", 10000, 305), ("Cah Kangkung - Warung Makan Pidade", 10000, 211), 
                                    ("Soto Madura - Depot Habbatussauda", 8000, 312), ("Mie ayam bakso - Bakso & Mie Ayam Barokah", 12000, 466), 
                                    ("Lalapan ayam tempong - Warung Bondowoso", 10000, 459), ("Perkedel kentang - Warung Muslim Mbak Siti", 5000, 107), 
                                    ("Capcay - Warung Nala", 10000, 120), ("Nasi ayam betutu - Nasi ayam betutu Tamkot", 12000, 490), 
                                    ("Gulai sapi - Stand Bu Haji", 10000, 271), ("Rendang sapi - Stand Bu Haji", 10000, 468)]
    uang_tersedia                   = int(input("Masukkan uang yang tersedia: "))
    perolehan_nutrisi, menu_anjuran = nutrition_measurement(menu_makanan, uang_tersedia)


    print("Kebutuhan nutrisi harian \t :", kebutuhan_nutrisi)
    print("Kebutuhan nutrisi yang diperoleh :", perolehan_nutrisi)
    print("Menu makanan yang dianjurkan \t :",menu_anjuran)


    if perolehan_nutrisi < kebutuhan_nutrisi:
        print("Kebutuhan gizi harian masih belum terpenuhi")
    elif perolehan_nutrisi == kebutuhan_nutrisi:
        print("Kebutuhan gizi harian telah terpenuhi")
    
mainProgram()