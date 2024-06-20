#!coding=utf8
from __future__ import print_function

import codecs
import sys
from argparse import ArgumentParser

import tensorflow as tf

from tagger import Model

import cws as TASK


class FlushFile:
    """
    A wrapper for File, allowing users see result immediately.
    """
    def __init__(self, f):
        self.f = f

    def write(self, x):
        self.f.write(x)
        self.f.flush()


if __name__ == '__main__':
    sys.stdout = FlushFile(sys.stdout)
    # 兼容tensorflow版本1中的session
    tf.compat.v1.disable_eager_execution()
    parser = ArgumentParser()
    parser.add_argument('--task', dest='task')
    parser.add_argument('--training_path', dest='training_path', default='data/datasets/sighan2005-pku/train.txt')
    parser.add_argument('--dev_path', dest='dev_path', default='data/datasets/sighan2005-pku/dev.txt')
    parser.add_argument('--test_path', dest='test_path', default='data/datasets/sighan2005-pku/test.txt')
    parser.add_argument('--pre_trained_emb_path', dest='pre_trained_emb_path', default=None)
    parser.add_argument('--pre_trained_word_emb_path', dest='pre_trained_word_emb_path', default=None)
    parser.add_argument('--model_root', dest='model_root', default='model-pku')
    parser.add_argument('--emb_size', dest='emb_size', type=int, default=200)
    parser.add_argument('--word_window', dest='word_window', type=int, default=0)
    parser.add_argument('--hidden_layers', dest='hidden_layers', type=int, default=5)
    parser.add_argument('--channels', dest='channels', type=int, default=200)
    parser.add_argument('--kernel_size', dest='kernel_size', type=int, default=3)
    parser.add_argument('--word_emb_size', dest='word_emb_size', type=int, default=50)
    parser.add_argument('--use_bn', dest='use_bn', type=int, default=0)
    parser.add_argument('--use_wn', dest='use_wn', type=int, default=1)
    parser.add_argument('--dropout_emb', dest='dropout_emb', type=float, default=0.2)
    parser.add_argument('--dropout_hidden', dest='dropout_hidden', type=float, default=0.2)
    parser.add_argument('--active_type', dest='active_type', default='glu')
    parser.add_argument('--lamd', dest='lamd', type=float, default=0)
    parser.add_argument('--fix_word_emb', dest='fix_word_emb', type=int, default=0)
    parser.add_argument('--reserve_all_word_emb', dest='reserve_all_word_emb', type=int, default=0)
    parser.add_argument('--use_crf', dest='use_crf', type=int, default=1)
    parser.add_argument('--optimizer', dest='optimizer', default='adam_0.001')
    parser.add_argument('--batch_size', dest='batch_size', type=int, default=100)
    parser.add_argument('--eval_batch_size', dest='eval_batch_size', type=int, default=1000)
    parser.add_argument('--max_epoches', dest='max_epoches', type=int, default=100)

    args = parser.parse_args()  # 解析收集入参
    print(args)  # 打印参数
    """
    __import__函数
    语法：__import__(name, globals=None, locals=None, fromlist=(), level=0)
    功能：按照name参数导入依赖包
    参数说明：
        name：依赖包名称
        globals和locals：用以决定如何在该依赖包的上下文解释该名称？
        fromlist：指出从该依赖包导入的对象或子模块的名称
        level：指定导入方式是绝对导入还是相对导入。0【默认值】表示绝对导入，正数表示相对于当前目录，将要搜索的父目录层数
    """
    # 此处替换为import cws as TASK
    # TASK = __import__(args.task)
    # 读取数据集，包括训练集、评估集、测试集
    """
    codecs：该模块定义了标准python编解码器的基类并提供对内部python编解码器注册表的访问
    codecs.open(filename, mode='r', encoding=None, errors='strict', buffering=-1)
    功能：使用给定的mode打开已编码的文件并返回一个SteamReaderWriter实例，提供透明的编码/解码
    参数说明：
        filename：文件路径
        mode：文件模式，默认为'r'，表示以读取模式打开文件
            文件模式参数值列表
            'r' 读取（默认）
            'w' 写入，并先截断文件【清空内容】
            'x' 排它性创建，如果文件已存在则失败
            'a' 打开文件用于写入，如果文件存在则在末尾追加
            'b' 二进制模式
            't' 文本模式（默认）
            '+' 打开用于更新（读取与写入）
        encoding：表示文件所要使用的编码格式
        errors：定义错误处理方案，默认'strict'，表示出现编码错误时引发ValueError
        buffer：一个可选的整数，用于设置缓冲策略。0表示关闭缓冲【仅在二进制模式下允许】，1表示行缓冲【仅在文本模式下写入时可用】，大于1的整数表示固定大小的块缓冲区的字节大小，-1表示使用默认的缓冲区大小
    """
    train_data, dev_data, test_data = (TASK.read_train_file(codecs.open(args.training_path, 'r', 'utf8'), word_window=args.word_window),
                                       TASK.read_train_file(codecs.open(args.dev_path, 'r', 'utf8'), word_window=args.word_window),
                                       TASK.read_train_file(codecs.open(args.test_path, 'r', 'utf8'), word_window=args.word_window))
    # 创建一个tensorflow会话，在会话内训练模型
    """
    tensorflow的运行机制：定义与运行相分离，tensorflow定义的内容都在“图”这个容器中完成。
    关于图的理解：
    1、一个图代表一个计算任务
    2、在模型运行的环节，图在会话【session】里被启动
    3、session将图的节点操作发布到CPU、GPU上，同时提供OP的方法
    也就是说在tensorflow中定义的时候，其实就只是定义了图，图是静态的，在定义完成之后是不会运行的。
    要想执行图中的节点操作，就需要使用运行函数 tf.Session.run，才能开始运行。
    代码样例请见当前目录下的tensorflow_learn.py
    """
    # sess = tf.Session()
    sess = tf.compat.v1.Session()
    model = Model(TASK.scope, sess)
    # 训练模型
    model.train(train_data=train_data,
                dev_data=dev_data,
                test_data=test_data,
                model_dir=args.model_root + '/models',
                log_dir=args.model_root + '/logs',
                emb_size=args.emb_size,
                word_emb_size=args.word_emb_size,
                hidden_layers=args.hidden_layers,
                channels=[args.channels] * args.hidden_layers,
                kernel_size=args.kernel_size,
                use_bn=args.use_bn,
                use_wn=args.use_wn,
                active_type=args.active_type,
                batch_size=args.batch_size,
                use_crf=args.use_crf,
                lamd=args.lamd,
                dropout_emb=args.dropout_emb,
                dropout_hidden=args.dropout_hidden,
                optimizer=args.optimizer,
                evaluator=TASK.evaluator,
                eval_batch_size=args.eval_batch_size,
                print_freq=50,
                pre_trained_emb_path=args.pre_trained_emb_path,
                pre_trained_word_emb_path=args.pre_trained_word_emb_path,
                fix_word_emb=args.fix_word_emb,
                reserve_all_word_emb=args.reserve_all_word_emb,
                max_epoches=args.max_epoches)
    # 关闭会话
    sess.close()
