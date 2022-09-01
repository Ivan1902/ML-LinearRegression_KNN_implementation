import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'nedeljkovic1',
        database = 'polovniautomobili'
    )
curr = conn.cursor()


# A)
curr.execute("""select city, count(*) as count
    from polovni_automobili
    group by city
    order by count(*) desc
    limit 10""")

df = pd.DataFrame(curr.fetchall(), columns=['city', 'count'])
plt.bar(df['city'], df['count'])
plt.xticks(rotation=90)
plt.title('10 najzastupljenijih lokacija koje imaju najveći broj automobila u ponudi')
plt.tight_layout()
plt.show()

# B)

curr.execute("""select sum(case when kilometers < 50000  then 1 else 0 end),
    sum(case when (kilometers >= 50000 and kilometers <= 99999) then 1 else 0 end),
    sum(case when (kilometers >= 100000 and kilometers <= 149999) then 1 else 0 end),
    sum(case when (kilometers >= 150000 and kilometers <= 199999) then 1 else 0 end),
    sum(case when (kilometers >= 200000 and kilometers <= 249999) then 1 else 0 end),
    sum(case when (kilometers >= 250000 and kilometers <= 299999) then 1 else 0 end),
    sum(case when kilometers >= 300000 then 1 else 0 end)
    from polovni_automobili
    """)

row = curr.fetchone()
counts = []
for data in row:
        counts.append(int(data))
plt.xticks(rotation=45, ha='right')
plt.title('Broj automobila prema kilometraži')
plt.bar(['x<50000km', '50000km<=x<=99999km', '100000km<=x<=149999km', '150000km<=x<=199999km', '200000km<=x<=249999km', '250000km<=x<=299999km', 'x>=300000km'], counts)
plt.tight_layout()
plt.show() #plt.savefig("filename.png")

# C)

curr.execute("""select sum(case when productionYear < 1960  then 1 else 0 end),
    sum(case when (productionYear >= 1961 and productionYear <= 1970) then 1 else 0 end),
    sum(case when (productionYear >= 1971 and productionYear <= 1980) then 1 else 0 end),
    sum(case when (productionYear >= 1981 and productionYear <= 1990) then 1 else 0 end),
    sum(case when (productionYear >= 1991 and productionYear <= 2000) then 1 else 0 end),
    sum(case when (productionYear >= 2001 and productionYear <= 2005) then 1 else 0 end),
    sum(case when (productionYear >= 2006 and productionYear <= 2010) then 1 else 0 end),
    sum(case when (productionYear >= 2011 and productionYear <= 2015) then 1 else 0 end),
    sum(case when (productionYear >= 2016 and productionYear <= 2020) then 1 else 0 end),
    sum(case when (productionYear >= 2021 and productionYear <= 2022) then 1 else 0 end)
    from polovni_automobili
    """)

row = curr.fetchone()
counts = []
for data in row:
        counts.append(int(data))
plt.xticks(rotation=45, ha='right')
plt.title('Broj automobila po godini proizvodnje')
plt.bar(['x<1960', '1961<=x<=1970', '1971<=x<=1980', '1981<=x<=1990', '1991<=x<=2000', '2001<=x<=2005', 
    '2006<=x<=2010','2011<=x<=2015','2016<=x<=2020','2021<=x<=2022'], counts)
plt.tight_layout()
plt.show()

# D)

curr.execute("""select count(*) as count
    from polovni_automobili
    where gearshift = 1
    union
    select count(*)
    from polovni_automobili
    where gearshift = 0 """)

counts = []
result = curr.fetchall()
for row in result:
    for data in row:
        counts.append(int(data))
procents = [counts[0]/(counts[0] + counts[1])*100, counts[1]/(counts[0] + counts[1])*100]
plt.xticks(rotation=0)
plt.title('Broj automobila sa manuelnim ili automatskim menjačem')
plt.bar(['Automatski menjac', 'Manuelni menjac'], counts)
plt.tight_layout()
plt.show()

plt.title('Procentualni odnos automobila sa manuelnim ili automatskim menjačem')
plt.bar(['Automatski menjac', 'Manuelni menjac'], procents)
plt.show()

#E)

curr.execute("""select sum(case when price < 2000  then 1 else 0 end),
    sum(case when (price >= 2000 and price <= 4999) then 1 else 0 end),
    sum(case when (price >= 5000 and price <= 9999) then 1 else 0 end),
    sum(case when (price >= 10000 and price <= 14999) then 1 else 0 end),
    sum(case when (price >= 15000 and price <= 19999) then 1 else 0 end),
    sum(case when (price >= 20000 and price <= 24999) then 1 else 0 end),
    sum(case when (price >= 25000 and price <= 29999) then 1 else 0 end),
    sum(case when (price >= 30000 ) then 1 else 0 end)
    from polovni_automobili
    """)

counts = []
procents = []
sum = 0
row = curr.fetchone()
for data in row:
    counts.append(int(data))
    sum += int(data)
for i in range(len(counts)):
    procents.append(float(counts[i]/sum*100))

plt.xticks(rotation=45, ha='right')
plt.title('Broj automobila koji po ceni pripadaju nekom od opsega')
plt.bar(['x<2000€', '2000€<=x<=4999€', '5000€<=x<=9999€', '10000€<=x<=14999€', 
    '15000€<=x<=19999€', '20000€<=x<=24999€', '25000€<=x<=29999€', 'x>=30000€'], counts)
plt.tight_layout()
plt.show()

plt.xticks(rotation=45, ha='right')
plt.title('Procentualni odnos automobila koji po ceni pripadaju nekom od opsega')
plt.bar(['x<2000€', '2000€<=x<=4999€', '5000€<=x<=9999€', '10000€<=x<=14999€', 
    '15000€<=x<=19999€', '20000€<=x<=24999€', '25000€<=x<=29999€', 'x>=30000€'], procents)
plt.tight_layout()
plt.show()

