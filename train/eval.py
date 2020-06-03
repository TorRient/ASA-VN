import torch
import numpy as np

def eval(model, data_loader, criterion=None):
    total_samples = 0
    correct_samples = 0
    total_loss = 0
    TP = np.array([0,0,0]) # Nhãn 0 - 1 - 2
    FP = np.array([0,0,0])
    real = np.array([0,0,0]) # Tổng nhãn thực
    model.eval()
    with torch.no_grad():
        for data in data_loader:
            input0, input1, label = data
            input0, input1, label = input0.cuda(), input1.cuda(), label.cuda()
            # print(input0.size(0))
            # print(label.data.tolist())
            # exit()
            logit = model(input0, input1)
            loss = criterion(logit, label).item() if criterion is not None else 0
            total_samples += input0.size(0)
            pred = logit.argmax(dim=1)
            correct_samples += (label == pred).long().sum().item()
            total_loss += loss * input0.size(0)

            label_l = label.data.tolist()
            pred_l = pred.data.tolist()
            for idx in range(len(label_l)):
                if pred_l[idx] == 0:
                    if label_l[idx] == 0:
                        TP[0] += 1
                    else:
                        FP[0] += 1
                elif pred_l[idx] == 1:
                    if label_l[idx] == 1:
                        TP[1] += 1
                    else:
                        FP[1] += 1
                else:
                    if label_l[idx] == 2:
                        TP[2] += 1
                    else:
                        FP[2] += 1
                real[label_l[idx]] += 1
    accuracy = correct_samples / total_samples
    avg_loss = total_loss / total_samples

    precision = TP/(TP+FP)
    recall = TP/real
    micro_p = np.sum(TP)/(np.sum(TP) + np.sum(FP))
    micro_r = np.sum(TP)/(np.sum(real))
    macro_p = np.sum(precision)/3
    macro_r = np.sum(recall)/3
    # print(TP)
    # print(FP)
    # print(real)
    # print(precision)
    print(recall)
    print("Micro Precision: ", micro_p)
    print("Micro Recall: ", micro_r)
    print("Macro Precision: ", macro_p)
    print("Macro Recall: ", macro_r)
    if criterion is not None:
        return accuracy, avg_loss
    else:
        return accuracy