# encoding=utf-8
from base.spark_base import spark_context, sql_context, spark_session
from spark.segment.dag import SparkDAGSegger
from spark.segment.hmm import SparkHMMSegger


dag_segger = SparkDAGSegger(context=spark_context)
hmm_segger = SparkHMMSegger(context=spark_context)

dag_segger.load()
hmm_segger.load()


def __get_single_end(word_list):
    i = 0
    while i < len(word_list):
        word = word_list[i]
        if len(word) > 1:
            return i
        i += 1
    return i


def __merge(seq):
    txt = u""
    for item in seq:
        txt += item
    return txt


def joint_cut(sentence):
    final_list = []
    word_list = dag_segger.cut(sentence)

    i = 0
    while i < len(word_list):
        word = word_list[i]
        if len(word) > 1:
            final_list.append(word)
            i += 1
        else:
            j = i + __get_single_end(word_list[i:])
            if i + 1 == j:
                final_list.append(word)
                i += 1
            else:
                second = __merge(word_list[i:j])
                second_list = hmm_segger.cut(second)
                final_list.extend(second_list)
                i = j

    return final_list


def dict_cut(sentence):
    return dag_segger.cut(sentence)


def hmm_cut(sentence):
    return hmm_segger.cut(sentence)

cut = joint_cut


def test():
    cases = [
        "我来到北京清华大学",
        "长春市长春节讲话",
        "我们在野生动物园玩",
        "我只是做了一些微小的工作",
        "国庆节我在研究中文分词",
        "比起生存还是死亡来忠诚与背叛可能更是一个问题"
    ]
    for case in cases:
        result = cut(case)
        for word in result:
            print(word)
        print('')

if __name__ == '__main__':
    test()
