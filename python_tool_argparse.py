from argparse import ArgumentParser

"""
argparse 是一个python模块，表示：命令行选项、参数和子命令解析器
功能有三：
    1、argparse模块可以让开发者轻松编写用户友好的命令行接口，支持程序定义其所需参数
    2、argparse将弄清如何从sys.argv解析出那些参数
    3、argparse模块可以自动生成帮助和使用手册，并在用户给程序输入无效参数时给出错误信息
使用流程：
    1、创建解析器：parser = argparse.ArgumentParser(description='Process some integers.')
    2、添加参数：parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    3、解析参数：parser.parse_args(['--sum', '7', '-1', '42'])
    Namespace(accumulate=<built-in function sum>, integers=[7, -1, 42])

"""

if __name__ == '__main__':
    # 举例：获取一个整数列表并计算总和或者最大值
    parser = ArgumentParser(description='process some integers')
    # accumulator 累加器
    # 添加参数
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    parser.add_argument('-sum', dest='accumulate', action='store_const', const=sum, default=max,
                        help='sum the integers (default: find the max)')
    args = parser.parse_args()
    print(args.accumulate(args.integers))
