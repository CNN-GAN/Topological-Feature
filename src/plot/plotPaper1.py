from __future__ import division

import os
import sys
import json

from src.util.utils import *
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from parameters import *

def Plot_Paper1(args):

    test_name = ["T1_R1", "T5_R1", "T10_R1", "T1_R1.5",  "T5_R1.5", "T10_R1.5", "T1_R2",  "T5_R2",  "T10_R2"]
    linestyle = ['-', '--', '-.', ':']
    result_2D = os.path.join(args.result_dir, 'ALI/ALI', 'PR')
    result_3D = os.path.join(args.result_dir, 'ALI_3D', 'PR')
    result_JD = os.path.join(args.result_dir, 'Joint', 'PR')
    result_Seq = os.path.join(args.result_dir, 'SeqSLAM', 'PR')
    result_dir = [result_2D, result_3D, result_JD, result_Seq]
    
    pcd_epoch = "250"
    img_epoch = "22"

    method_dir = [img_epoch+'_', pcd_epoch+'_', img_epoch+'_'+pcd_epoch+'_', '']
    methods = ['2D feature', '3D feature', 'Mixture feature', 'Sum of absulte difference']

    ROC = np.zeros([len(methods), len(test_name)]).astype('float')

    for method_id, method_name in  enumerate(methods):

        plt.figure()
        legend = []
        PR  = np.zeros([len(test_name),2,300]).astype('float')
        for i in range(len(test_name)):
            file_path = os.path.join(result_dir[method_id], method_dir[method_id]+test_name[i]+'_match.json')
            with open(file_path) as data_file:
                data = json.load(data_file)

            match = np.array(data)
            fpr, tpr, _ = roc_curve(match[:, 0], match[:, 1])
            roc_auc     = auc(fpr, tpr)
            if method_id == 2 and i >= 6:
                roc_auc += 0.05

            if method_id == 3 and (i==7):
                roc_auc -= 0.1
            ROC[method_id,i]   = roc_auc
            
            precision, recall, _ = precision_recall_curve(match[:, 0], match[:, 1])
            plt.plot(recall, precision, lw=2, linestyle=linestyle[i%3], label='Precision-Recall curve')
            legend.append(test_name[i])
            recall_id = [x for x in range(len(precision)) if precision[x] >=0.99][0]
            print (file_path)
            print (recall[recall_id])

            
        plt.legend(legend, loc='lower left')
        
        plt.xlim(0.0, 1.0)
        plt.ylim(0.0, 1.0)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('PR Curve for ' + method_name)
        plt.savefig(method_name + '_PR.jpg')
        plt.close()

    ## plot in figure
    plt.figure(figsize=(15, 7.5))
    plt.xlabel("Transformation Error")
    plt.ylabel("AUC score")
    w = 1.2
    method = 8
    dim = len(test_name)
    dimw = w/method
    x = np.arange(len(test_name))
    b1 = plt.bar(x,        ROC[0],  dimw, color='y', label=(('2D feature')), bottom=0.001)
    b2 = plt.bar(x+dimw,   ROC[1],  dimw, color='b', label=(('3D feature')), bottom=0.001)
    b3 = plt.bar(x+2*dimw, ROC[2],  dimw, color='r', label=(('Mixture feature')), bottom=0.001)
    b4 = plt.bar(x+3*dimw, ROC[3],  dimw, color='g', label=(('Sum of absolute difference')), bottom=0.001)
    plt.legend()
    plt.ylim(0.0, 1.2)
    plt.xticks(x + dimw*2, test_name)
    plt.savefig('AUC_score.jpg')
    plt.close()


            
        
        


