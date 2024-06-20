import tensorflow as tf

if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    # 定义一个常量
    hello = tf.constant('hello, tensorflow')
    # 建立一个session
    session = tf.compat.v1.Session()
    # 通过session中的run函数运行hello这个变量
    print(session.run(hello))
    # 关闭session
    session.close()
