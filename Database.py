import pymysql


class Database(object):

    conn = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if Database.conn is None:
            self.__connect_to_db()

    def __connect_to_db(self):
        Database.conn = pymysql.connect(host='176.99.7.62', port=3306, user='wms', passwd='y7cH7nw64dFKPUqX23', db='wms')
        self.cur = Database.conn.cursor()

    def get_products(self, count):
        self.cur.execute('SELECT product_id, sku_num FROM sku inner join sku_warehouse on sku.id = sku_warehouse.variant_id where sku_warehouse.stock>0 LIMIT %s' % count)
        products=self.cur.fetchall()
        return products

    def get_variants(self,count=None):
        if count is None:
            self.cur.execute('SELECT id FROM sku')
        else:
            self.cur.execute('SELECT id FROM sku LIMIT %s' % count)
        products = self.cur.fetchall()
        variants = [item[0] for item in products]
        return variants

    def count_in_table(self, table_name):
        self.cur.execute('select count(*) from %s' % table_name)
        count = self.cur.fetchall()[0][0]
        return count

    def get_next_order_id(self):
        self.cur.execute('select platform_order_id FROM order ORDER BY id desc')
        return int(self.cur.fetchall()[0][0]) + 1