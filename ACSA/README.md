### ACSA for VN
Aspect-category sentiment analysis

### Requirements

```
pytorch==1.1.0
adabound==0.0.5
pyyaml==5.1.2
numpy==1.17.2
vncorenlp==1.0.3
```
# Download model VNCoreNLP

https://github.com/vncorenlp/VnCoreNLP/archive/master.zip


### Pretrained Word2Vec

Download Word2Vec https://drive.google.com/file/d/1LV9z1RXkEg0niuC15jcW2JeeYDilXiiC/view

Extract and put in folder word2vec

### Prepare data (Option)

Option: vì nhóm đã xử lý và đặt dữ liệu trong thư mục dataset/raw

Nguồn data: https://vlsp.org.vn/vlsp2018/eval/sa

```bash
mkdir VLSP2018
```

Put file txt in folder VLSP2018

```bash
python prepare_datavlsp.py
```

### Preprocess data

```bash
python preprocess.py
```

### How to train

```bash
python train.py
```

### How to test

1. You must Preprocess data before

2. Download pretrained model and put in folder model

https://drive.google.com/file/d/1cRPkOveo2jo4oy9J_bjCWEjLjdxKFlwh/view?usp=sharing

3. Run test.py

```bash
python test.py
```

### Result

|   Accuracy  |   Macro F1  | Macro Precision |  Macro Recall |
| :---------: | :---------: |  :-----------:  |  :---------:  |
|    0.7950   |    0.6662   |     0.6709      |     0.6616    |
