import torch
import os
from train import  make_aspect_category_model
from train.make_data import make_category_test_data
from train.eval import eval

def test(config):
    mode = config['mode']
    model = make_aspect_category_model.make_model(config)

    model = model.cuda()
    model_path = os.path.join(config['base_path'], 'checkpoints/%s.pth' % config['aspect_' + mode + '_model']['type'])
    model.load_state_dict(torch.load(model_path))

    test_loader = make_category_test_data(config)
    accuracy, micro_r, macro_p, macro_r, macro_f1 = eval(model, test_loader)
    print('Accuracy: %.4f' % (accuracy))
    print('Micro: %.4f' % (micro_r))
    print('Macro Precision: %.4f' % (macro_p))
    print('Macro Recall: %.4f' % (macro_r))
    print('Macro F1: %.4f' % (macro_f1))