import pycorrector
pycorrector.en_correct("helio")


from pycorrector.ernie.ernie_corrector import ErnieCorrector
'''
if __name__ == '__main__':
    error_sentences = [
        '真麻烦你了。希望你们好好的跳无',
        '少先队员因该为老人让坐',
        '机七学习是人工智能领遇最能体现智能的一个分知',
        '一只小鱼船浮在平净的河面上',
        '我的家乡是有明的渔米之乡',
    ]

    m = ErnieCorrector()
    for line in error_sentences:
        correct_sent, err = m.ernie_correct(line)
        print("original sentence:{} => {}, err:{}".format(line, correct_sent, err))
'''

import pandas as pd

error_sentences = pd.read_csv(r'D:\BaiduNetdiskDownload\文本赛题-测试集a\testa.csv')
error_sentences = pd.DataFrame(error_sentences)
test = error_sentences.head(10)

model = ErnieCorrector()
for line in test['err_text']:
    correct_sent = model.ernie_correct(line)
    print(correct_sent)

correct_sent[0]