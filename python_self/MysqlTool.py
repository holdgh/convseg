import pymysql

"""
Python 的 with 语句支持通过上下文管理器所定义的运行时上下文这一概念。 此对象的实现使用了一对专门方法，允许用户自定义类来定义运行时上下文，在语句体被执行前进入该上下文，并在语句执行完毕时退出该上下文：

contextmanager.__enter__()

    进入运行时上下文并返回此对象或关联到该运行时上下文的其他对象。 此方法的返回值会绑定到使用此上下文管理器的 with 语句的 as 子句中的标识符。

    一个返回其自身的上下文管理器的例子是 file object。 文件对象会从 __enter__() 返回其自身，以允许 open() 被用作 with 语句中的上下文表达式。

    一个返回关联对象的上下文管理器的例子是 decimal.localcontext() 所返回的对象。 此种管理器会将活动的 decimal 上下文设为原始 decimal 上下文的一个副本并返回该副本。 这允许对 with 
    语句的语句体中的当前 decimal 上下文进行更改，而不会影响 with 语句以外的代码。

contextmanager.__exit__(exc_type, exc_val, exc_tb)

    退出运行时上下文并返回一个布尔值旗标来表明所发生的任何异常是否应当被屏蔽。 如果在执行 with 语句的语句体期间发生了异常，则参数会包含异常的类型、值以及回溯信息。 在其他情况下三个参数均为 None。

    自此方法返回一个真值将导致 with 语句屏蔽异常并继续执行紧随在 with 语句之后的语句。 否则异常将在此方法结束执行后继续传播。 在此方法执行期间发生的异常将会取代 with 语句的语句体中发生的任何异常。

    传入的异常绝对不应当被显式地重新引发 —— 相反地，此方法应当返回一个假值以表明方法已成功完成并且不希望屏蔽被引发的异常。 这允许上下文管理代码方便地检测 __exit__() 方法是否确实已失败。

"""


class MysqlTool:
    # 初始化方法，创建类对象时执行，类似Java的构造函数
    def __init__(self, host='', port=3306, user='root', password='cp7R@1K59t3C#Hl4', db='python_test', charset='utf8'):
        """mysql 连接初始化"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.mysql_conn = None

    # 与with……as结合使用，用于进入时执行
    def __enter__(self):
        """打开数据库连接"""
        self.mysql_conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset=self.charset
        )
        return self

    # 与with……as结合使用，用于退出时执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭数据库连接"""
        if self.mysql_conn:
            self.mysql_conn.close()
            self.mysql_conn = None

    def execute(self, sql: str, args: tuple = None, commit: bool = False) -> any:
        """执行 SQL 语句"""
        try:
            # 创建游标对象，类似于Java数据库连接中的sql会话对象
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    # 对于修改数据操作，例如增删改，需要在执行SQL后提交会话
                    self.mysql_conn.commit()
                    # print(f"执行 SQL 语句：{sql}，参数：{args}，数据提交成功")
                else:
                    # 对于查询操作，不需要提交，此处为获取查询结果
                    result = cursor.fetchall()
                    print(f"执行 SQL 语句：{sql}，参数：{args}，查询到的数据为：{result}")
                    return result
        except Exception as e:
            print(f"执行 SQL 语句出错：{e}")
            self.mysql_conn.rollback()
            raise e

    def insert_batch(self, sql: str, args: list = None) -> any:
        """batch执行 SQL 语句"""
        try:
            # 创建游标对象，类似于Java数据库连接中的sql会话对象
            with self.mysql_conn.cursor() as cursor:
                cursor.executemany(sql, args)
                # 对于修改数据操作，例如增删改，需要在执行SQL后提交会话
                self.mysql_conn.commit()
        except Exception as e:
            print(f"执行 SQL 语句出错：{e}")
            self.mysql_conn.rollback()
            raise e
