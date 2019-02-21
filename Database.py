import pymysql

class Database(object):

    conn = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if Database.conn is None:
            self.db_user = 'wms'
            self.database_ip = '176.99.7.62'
            self.db_port = 3306
            self.db_name = 'wms'
            self.__connect_to_db()

    def __connect_to_db(self):
        conn = pymysql.connect(host='176.99.7.62', port=3306, user='wms', passwd='y7cH7nw64dFKPUqX23', db='wms')
        self.cur = conn.cursor()

    def get_products(self, count):
        self.cur.execute('SELECT product_id, sku_num FROM sku LIMIT %s' % count)
        products=self.cur.fetchall()
        return products