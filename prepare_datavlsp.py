import argparse
from tqdm import tqdm
# from pyvi import ViTokenizer

parser = argparse.ArgumentParser()

parser.add_argument("--mode", default="restaurant", help="mode restaurant or hotel")

args = parser.parse_args()

if args.mode == "restaurant":
    train = './VLSP2018/1-VLSP2018-SA-Restaurant-train (7-3-2018).txt'
    dev = './VLSP2018/2-VLSP2018-SA-Restaurant-dev (7-3-2018).txt'
    test = './VLSP2018/3-VLSP2018-SA-Restaurant-test (8-3-2018).txt'

else:
    train = './VLSP2018/1-VLSP2018-SA-Hotel-train (7-3-2018).txt'
    dev = './VLSP2018/2-VLSP2018-SA-Hotel-dev (7-3-2018).txt'
    test = './VLSP2018/3-VLSP2018-SA-Hotel-test (8-3-2018).txt'

train_out = './VLSP2018/' + 'train.xml'
dev_out = './VLSP2018/' + 'val.xml'
test_out = './VLSP2018/' + 'test.xml'

def write_xml(path_txt, output):
    sentences = []
    label = []
    poli = []
    count = 0
    with open(path_txt, 'r') as files:
        for line in files:
            sentences.append(line)
    print(len(sentences))
    with open(output, 'w') as out:
        out.write('<?xml version="1.0" encoding="utf-8"?>')
        out.write('<sentences>')

        for idx in tqdm(range(int(len(sentences)/4) + 1)):
            start = '#' + str(idx+1)
            for line in sentences:
                if start in line:
                    # token = ViTokenizer.tokenize(str(sentences[idx*4+1]))
                    token = str(sentences[idx*4+1])
                    if len(token.split(' ')) > 512:
                        count += 1
                        continue
                    out.write('<sentence>')
                    out.write('<text>')
                    token = token.replace("&", 'và').replace("<", '&lt;').replace(">", '&gt;')
                    out.write(token)
                    out.write('</text>')
                    out.write('<aspectCategories>')
                    # print(sentences[idx+1])
                    for aspect in sentences[idx*4+2].split('}, '):
                        category, polarity = aspect.split(',')
                        category = category.replace('{','').replace(" ", '').replace("&", '')
                        polarity = polarity.replace('}','').replace(" ", '').replace("\n", '')
                        if category not in label:
                            label.append(category)
                        if polarity not in poli:
                            poli.append(polarity)
                        out.write('<aspectCategory category="{}" polarity="{}"/>'.format(category, polarity))
                    out.write('</aspectCategories>')
                    out.write('</sentence>')
                    break
        out.write('</sentences>')
    return label, poli, count
label, poli, count = write_xml(train, train_out)
write_xml(dev, dev_out)
write_xml(test, test_out)
print(label)
print(poli)
print(count)