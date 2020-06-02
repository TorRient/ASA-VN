import json

# sd = json.load(open('./data/sentiment_dict.json', 'r', encoding='utf-8'))
# sd['positive'] = set(sd['positive'])
# sd['negative'] = set(sd['negative'])
# sd['neutral'] = set(sd['neutral'])
# print(sd['positive'])



with open('./data/cc.vi.300.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # print(line)
        content = line.split(' ')
        word = content[0]
        # print(word)
        if word == u'khôngrẻ':
            print(content)
