# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector

class PolovniautomobiliPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'nedeljkovic1',
            database = 'polovniautomobili'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS polovni_automobili""")
        self.curr.execute("""CREATE TABLE polovni_automobili(
            brand text,
            city text,
            color text,
            price float,
            subcategory text,
            productionYear int,
            engineCapacity float,
            enginePower float,
            kilometers float,
            gearshift boolean,
            seatsNumber float,
            model text,
            new_used boolean,
            registrated boolean,
            engineClass text
        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into polovni_automobili values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item.get('brand'),
            item.get('city'),
            item.get('color'),
            item.get('price'),
            item.get('subcategory'),
            item.get('productionYear'),
            item.get('engineCapacity'),
            item.get('enginePower'),
            item.get('kilometers'),
            item.get('gearshift'),
            item.get('seatsNumber'),
            item.get('model'),
            item.get('new_used'),
            item.get('registrated'),
            item.get('engineClass')
        ))
        self.conn.commit()
