from __future__ import print_function

import codecs
import os
# python3中没有python2.7中的izip，这里采用python3自带的zip
# from itertools import izip

from tagger import data_iterator

scope = 'CWS'


def process_train_sentence(sentence, bigram, word_window):
    """
     str.strip([chars])

    返回原字符串的副本，移除其中的前导和末尾字符。 chars 参数为指定要移除字符的字符串。 如果省略或为 None，则 chars 参数默认移除空白符。 实际上 chars 参数并非指定单个前缀或后缀；而是会移除参数值的所有组合【最外侧的前导和末尾 chars 参数值将从字符串中移除。 开头端的字符的移除将在遇到一个未包含于 chars 所指定字符集的字符时停止。 类似的操作也将在结尾端发生。】
    """
    # 对句子前后做去空格处理
    sentence = sentence.strip()
    """
     str.split(sep=None, maxsplit=-1)

    返回一个由字符串内单词组成的列表，使用 sep 作为分隔字符串。 如果给出了 maxsplit，则最多进行 maxsplit 次拆分（因此，列表最多会有 maxsplit+1 个元素）。 如果 maxsplit 未指定或为 -1，则不限制拆分次数（进行所有可能的拆分）。

    如果给出了 sep，则连续的分隔符不会被组合在一起而是被视为分隔空字符串 (例如 '1,,2'.split(',') 将返回 ['1', '', '2'])。 sep 参数可能由多个字符组成 (例如 '1<>2<>3'.split('<>') 将返回 ['1', '2', '3'])。 使用指定的分隔符拆分空字符串将返回 ['']。
    
    如果 sep 未指定或为 None，则会应用另一种拆分算法：连续的空格会被视为单个分隔符，其结果将不包含开头或末尾的空字符串，如果字符串包含前缀或后缀空格的话。 因此，使用 None 拆分空字符串或仅包含空格的字符串将返回 []。
    """
    # 按空格拆分句子，得到分词列表
    words = sentence.split()
    chars = []
    tags = []
    ret = []
    # 遍历分词列表，逐分词处理
    for w in words:
        """
        list()其实是类list的构造器方法。
        可以用多种方式构建列表：
            使用一对方括号来表示空列表: []
            使用方括号，其中的项以逗号分隔: [a], [a, b, c]
            使用列表推导式: [x for x in iterable]
            使用类型的构造器: list() 或 list(iterable)
        构造器将构造一个列表，其中的项与 iterable 中的项具有相同的的值与顺序。 iterable 可以是序列、支持迭代的容器或其它可迭代对象。 如果 iterable 已经是一个列表，将创建并返回其副本，类似于 iterable[:]。 例如，list('abc') 返回 ['a', 'b', 'c'] 而 list( (1, 2, 3) ) 返回 [1, 2, 3]。 如果没有给出参数，构造器将创建一个空列表 []
        """
        # 将当前分词通过list()生成单词列表
        """
        列表对象的extend方法，s.extend(t) 或 s += t：用 t 的内容扩展 s
        例如：a=[],b=[1,2,3]
        a.extend(b)
        a=[1,2,3]
        """
        # 将当前分词对应的单词列表，追加到chars中
        chars.extend(list(w))
        # 按照分词长度，打标
        if len(w) == 1:
            # 如果当前分词仅包含一个单词，则打标S
            tags.append('S')
        else:
            # 如果当前分词包含多于一个单词，则打标追加['B', 【len(w) - 2个】'M', 'E']
            # B和E算作两个占位标识，对应len(w) - 2中减去的2，剩余的用M标记
            tags.extend(['B'] + ['M'] * (len(w) - 2) + ['E'])
    # 将当前句子的单词列表整体作为一个元素追加到ret中
    ret.append(chars)
    if bigram:
        chars = ['', ''] + chars + ['', '']
        ret.append([a + b if a and b else '' for a, b in zip(chars[:-4], chars[1:])])
        ret.append([a + b if a and b else '' for a, b in zip(chars[1:-3], chars[2:])])
        ret.append([a + b if a and b else '' for a, b in zip(chars[2:-2], chars[3:])])
        ret.append([a + b if a and b else '' for a, b in zip(chars[3:-1], chars[4:])])
    elif word_window > 0:
        chars = ['', '', ''] + chars + ['', '', '']
        # single char
        if word_window >= 1:
            ret.append(chars[3:-3])
        if word_window >= 2:
            # bi chars
            ret.append([a + b if a and b else '' for a, b in zip(chars[2:], chars[3:-3])])
            ret.append([a + b if a and b else '' for a, b in zip(chars[3:-3], chars[4:])])
        if word_window >= 3:
            # tri chars
            ret.append(
                [a + b + c if a and b and c else '' for a, b, c in zip(chars[1:], chars[2:], chars[3:-3])])
            ret.append(
                [a + b + c if a and b and c else '' for a, b, c in zip(chars[2:], chars[3:-3], chars[4:])])
            ret.append(
                [a + b + c if a and b and c else '' for a, b, c in zip(chars[3:-3], chars[4:], chars[5:])])
        if word_window >= 4:
            # four chars
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                            zip(chars[0:], chars[1:], chars[2:], chars[3:-3])])
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                            zip(chars[1:], chars[2:], chars[3:-3], chars[4:])])
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                            zip(chars[2:], chars[3:-3], chars[4:], chars[5:])])
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                             zip(chars[3:-3], chars[4:], chars[5:], chars[6:])])
    ret.append(tags)
    return ret


def process_raw_sentence(sentence, bigram, word_window):
    sentence = sentence.strip()
    chars = list(sentence)
    ret = [chars]
    if bigram:
        chars = ['', ''] + chars + ['', '']
        ret.append([a + b if a and b else '' for a, b in zip(chars[:-4], chars[1:])])
        ret.append([a + b if a and b else '' for a, b in zip(chars[1:-3], chars[2:])])
        ret.append([a + b if a and b else '' for a, b in zip(chars[2:-2], chars[3:])])
        ret.append([a + b if a and b else '' for a, b in zip(chars[3:-1], chars[4:])])
    elif word_window > 0:
        chars = ['', '', ''] + chars + ['', '', '']
        # single char
        if word_window >= 1:
            ret.append(chars[3:-3])
        if word_window >= 2:
            # bi chars
            ret.append([a + b if a and b else '' for a, b in zip(chars[2:], chars[3:-3])])
            ret.append([a + b if a and b else '' for a, b in zip(chars[3:-3], chars[4:])])
        if word_window >= 3:
            # tri chars
            ret.append(
                [a + b + c if a and b and c else '' for a, b, c in zip(chars[1:], chars[2:], chars[3:-3])])
            ret.append(
                [a + b + c if a and b and c else '' for a, b, c in zip(chars[2:], chars[3:-3], chars[4:])])
            ret.append(
                [a + b + c if a and b and c else '' for a, b, c in zip(chars[3:-3], chars[4:], chars[5:])])
        if word_window >= 4:
            # four chars
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                            zip(chars[0:], chars[1:], chars[2:], chars[3:-3])])
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                            zip(chars[1:], chars[2:], chars[3:-3], chars[4:])])
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                            zip(chars[2:], chars[3:-3], chars[4:], chars[5:])])
            ret.append([a + b + c + d if a and b and c and d else '' for a, b, c, d in
                             zip(chars[3:-3], chars[4:], chars[5:], chars[6:])])
    return ret


def read_train_file(fin, bigram=False, word_window=4):
    """
    Read training data.
    """
    data = []
    # 逐句处理
    for l in fin:
        # 读取当前句子，并收集读取结果
        data.append(process_train_sentence(l, bigram, word_window))
    # 对上述读取结果进行压缩，生成一个元组列表，每个元组的长度相等，为最短句子的字数
    """
    a=[[1, 2, 3], [1, 2, 3], [1, 2, 3, 4]]
    list(zip(*a))-->[(1, 1, 1), (2, 2, 2), (3, 3, 3)]
    """
    return zip(*data)


def read_raw_file(fin, batch_size, bigram=False, word_window=4):
    """
    Read raw data.
    """
    buffer = []
    max_buffer = 100000
    for i, l in enumerate(fin):
        buffer.append(process_raw_sentence(l, bigram, word_window))
        if i % max_buffer == 0 and i > 0:
            for b in data_iterator(zip(*buffer), batch_size, shuffle=False):
                yield b
            buffer = []
    if buffer:
        for b in data_iterator(zip(*buffer), batch_size, shuffle=False):
            yield b


def read_raw_file_all(fin, bigram=False, word_window=4):
    """
    Read raw data.
    """
    data = []
    for b in read_raw_file(fin, 1000, bigram, word_window):
        data.extend(zip(*b))
    return zip(*data)


def create_output(seqs, stags):
    """
    Create final output from characters and BMES tags.
    """
    output = []
    for seq, stag in zip(seqs, stags):
        new_sen = []
        for c, tag in zip(seq, stag):
            new_sen.append(c)
            if tag == 'S' or tag == 'E':
                new_sen.append('  ')
        output.append(''.join(new_sen))
    return output


def evaluator(data, output_dir, output_flag):
    """
    Evaluate presion, recall and F1.
    """
    seqs, gold_stags, pred_stags = data
    assert len(seqs) == len(gold_stags) == len(pred_stags)
    # Create and open temp files.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ref_path = os.path.join(output_dir, '%s.ref' % output_flag)
    pred_path = os.path.join(output_dir, '%s.pred' % output_flag)
    score_path = os.path.join(output_dir, '%s.score' % output_flag)
    # Empty words file.
    temp_path = os.path.join(output_dir, '%s.temp' % output_flag)

    ref_file = codecs.open(ref_path, 'w', 'utf8')
    pred_file = codecs.open(pred_path, 'w', 'utf8')
    for l in create_output(seqs, gold_stags):
        print(l, file=ref_file)
    for i, l in enumerate(create_output(seqs, pred_stags)):
        print(l, file=pred_file)
    ref_file.close()
    pred_file.close()

    os.system('echo > %s' % temp_path)
    os.system('%s  %s %s %s > %s' % ('./score.perl', temp_path, ref_path, pred_path, score_path))
    # Sighan evaluation results
    os.system('tail -n 7 %s > %s' % (score_path, temp_path))
    eval_lines = [l.rstrip() for l in codecs.open(temp_path, 'r', 'utf8')]
    # Remove temp files.
    os.remove(ref_path)
    os.remove(pred_path)
    os.remove(score_path)
    os.remove(temp_path)
    # Precision, Recall and F1 score
    return (float(eval_lines[1].split(':')[1]),
            float(eval_lines[0].split(':')[1]),
            float(eval_lines[2].split(':')[1]))