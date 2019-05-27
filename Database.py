import pymysql


class Database(object):

    conn = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.cur = None
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
        self.cur.execute('select platform_order_id FROM `order` ORDER BY id desc limit 1')
        cur_order = self.cur.fetchall()[0][0]
        print('Current order= %s' % cur_order)
        next_order =int(cur_order) + 1
        print('nex_order_id: %s' % next_order)
        return next_order

    def get_sku_weight(self, sku_num):
        self.cur.execute('select weight_net from `sku` where sku_num={0}'.format(sku_num))
        weight = int(self.cur.fetchone()[0])
        print('SKU {0} is weight = {1}'.format(sku_num,weight))
        return weight

    def get_order_weight(self, ext_order_id):
        self.cur.execute('select shp_weight from `order` where external_order_id={0}'.format(ext_order_id) )
        weight = int(self.cur.fetchone()[0])
        print('ext_order_id {0} is weight = {1}'.format(ext_order_id,weight))
        return weight

if __name__=='__main__':
    db = Database()
    db.get_next_order_id()