from tools.db_oprt_base import DataBaseOprt
import mysql.connector


class DataBaseOprtMySQL(DataBaseOprt):
    class DataBaseParams:

        class DB5:
            host = '0.0.0.5'
            port = '3306'
            user = 'steff'
            pwd = 'password'

        class DB11:
            host = '0.0.0.11'
            port = '3306'
            user = 'steff'
            pwd = 'password'

        class DB21:
            host = '0.0.0.21'
            port = '3306'
            user = 'steff'
            pwd = 'password'

        class DB29:
            host = '0.0.0.29'
            port = '3306'
            user = 'steff'
            pwd = 'password'

        class DB32:
            host = '0.0.0.32'
            port = '3306'
            user = 'steff'
            pwd = 'password'

        class DB42:
            host = '0.0.0.42'
            port = '3306'
            user = 'steff'
            pwd = 'password'

    class SQL:
        sql_get_com = "select commission_json from tradingconfigdb.t_simple_general_commission_template " \
                      "where `name`='测试标准模板'"
        sql_get_fees = "SELECT fee_rate from tradingconfigdb.t_simple_fixed_fee " \
                       "where fee_type = '{0}' " \
                       "and trade_type = '{1}' " \
                       "and security_type = '{2}' " \
                       "and market_id = '{3}'"

    class OperateDB:
        def __init__(self, conn_params_obj, db='testdb'):
            self.conn = mysql.connector.connect(
                host=conn_params_obj.host,
                port=conn_params_obj.port,
                user=conn_params_obj.user,
                passwd=conn_params_obj.pwd,
                db=db,
                charset='utf8')
            self.cur = self.conn.cursor()

        def execute_query(self, sql):
            try:
                self.cur.execute(sql)
                result = self.cur.fetchall()
                print(result)
                # a = ("{0}".format(result))
                # b = re.findall(r"\d+.?\d*", a)
                # return b
            except mysql.connector.Error as e:
                print('query error!{}'.format(e))
            finally:
                print('end')
                self.close()

        def close(self):
            self.cur.close()
            self.conn.close()
