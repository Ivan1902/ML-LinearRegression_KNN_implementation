# ovo ide u konzolu
# chcp 65001
# set PYTHONIOENCODING=utf-8
import mysql.connector


conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'nedeljkovic1',
        database = 'polovniautomobili'
    )
curr = conn.cursor()

# A)
print("======================================================")
print("Broj automobila za svaku od dostupnih marki:")

curr.execute("""select brand as 'Marka', count(*) as 'Broj automobila'
    from polovni_automobili
    group by brand""")

for row in curr:
    print(row)

#B) 
print("======================================================")
print("Broj automobila u svakom od gradova:")

curr.execute("""select city as 'Grad', count(*) as 'Broj automobila'
    from polovni_automobili
    group by city""")

for row in curr:
    print(row)

#C) 
print("======================================================")
print("Broj automobila po bojama:")

curr.execute("""select color as 'Boja', count(*) as 'Broj automobila'
    from polovni_automobili
    group by color""")

for row in curr:
    print(row)

#D) 
print("======================================================")
print("Rang lista prvih 30 najskupljih automobila koji se prodaju:")

curr.execute("""select brand, model, price
    from polovni_automobili
    order by price desc
    limit 30""")

for row in curr:
    print(row)

print("Rang lista prvih 30 najskupljih automobila iz potkategorije džipovi/SUV:")

curr.execute("""select brand, model, price
    from polovni_automobili
    where subcategory = 'džip/SUV'
    order by price desc
    limit 30""")

for row in curr:
    print(row)

#E) 
print("======================================================")
print("Rang lista svih automobila proizvedenih 2021. i 2022. godine, sortirana opadajuće prema ceni:")

curr.execute("""select brand, model, price, productionYear
    from polovni_automobili
    where productionYear = 2021 or productionYear = 2022
    order by price desc""")

# if(len(list(curr)) == 0):
#     print('Nema podataka za prikaz!')
for row in curr:
    print(row)

#F) 
print("======================================================")
print("Automobil koji ima najvecu kubikazu:")
curr.execute("""select brand, model, CONCAT(engineCapacity, ' cm3')
    from polovni_automobili
    where engineCapacity = (select MAX(engineCapacity) from polovni_automobili)""")

for row in curr:
    print(row)

print("Automobil koji ima najvecu snagu motora:")
curr.execute("""select brand, model, CONCAT(enginePower, ' kW')
    from polovni_automobili
    order by enginePower desc
    limit 1""")

for row in curr:
    print(row)

print("Automobil koji ima najvecu kilometrazu:")
curr.execute("""select brand, model, CONCAT(kilometers, ' km')
    from polovni_automobili
    order by kilometers desc
    limit 1""")

for row in curr:
    print(row)