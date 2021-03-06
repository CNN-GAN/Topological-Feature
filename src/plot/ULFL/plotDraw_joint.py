from __future__ import division

import os
import sys
import json

from src.util.utils import *
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from parameters import *

def Plot_Joint(args):

    test_dir = ["T1_R1", "T1_R1.5", "T1_R2",  "T5_R1", "T5_R1.5", "T5_R2",  "T10_R1", "T10_R1.5", "T10_R2", "T20_R1", "T20_R1.5", "T20_R2"]

    result_img = os.path.join(args.result_dir, 'ALI/ALI')
    result_pcd = os.path.join(args.result_dir, 'ALI_3D')
    result_dir = os.path.join(args.result_dir, 'Joint')
    matrix_dir = os.path.join(result_dir,      'MATRIX')
    pr_dir     = os.path.join(result_dir,      'PR')
    match_dir  = os.path.join(result_dir,      'MATCH')
    pose_dir   = os.path.join(args.data_dir,   'new_loam', '00')
    
    pcd_epoch = "250"
    img_epoch = "22"    

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)   
        
    if not os.path.exists(matrix_dir):
        os.makedirs(matrix_dir)       

    if not os.path.exists(pr_dir):
        os.makedirs(pr_dir)   

    if not os.path.exists(match_dir):
        os.makedirs(match_dir)   

    Trainvector_img = os.path.join(result_img, img_epoch+'_gt_vt.npy')
    Trainvector_pcd = os.path.join(result_pcd, pcd_epoch+'_gt_vt.npy')
    train_img = np.load(Trainvector_img)
    train_pcd = np.load(Trainvector_pcd)*1.0
    train_code = np.concatenate((train_img, train_pcd), axis=1)

    Trainvector_pose = os.path.join(pose_dir, 'gt', 'pose.txt')
    train_pose = np.loadtxt(Trainvector_pose)
    train_pose = train_pose[0:args.test_len*args.frame_skip:args.frame_skip, 1:3]

    for file_id, file_name in enumerate(test_dir):
        print('Load data file:{}'.format(file_name)) 
        Testvector_img = os.path.join(result_img, img_epoch+'_'+file_name+'_vt.npy')
        Testvector_pcd = os.path.join(result_pcd, pcd_epoch+'_'+file_name+'_vt.npy')
        test_img = np.load(Testvector_img)*1.0
        test_pcd = np.load(Testvector_pcd)*1.0
        test_code = np.concatenate((test_img, test_pcd), axis=1)     

        Testvector_pose = os.path.join(pose_dir, file_name, 'pose.txt')
        test_pose = np.loadtxt(Testvector_pose)
        test_pose = test_pose[0:args.test_len*args.frame_skip:args.frame_skip, 1:3]        

        D = Euclidean(train_code, test_code)
        #D = Cosine(train_code, test_code)
        DD = enhanceContrast(D, 30)
        DD_sub = DD[150:200, 150:200]    

        print (D.shape)
        scipy.misc.imsave(os.path.join(matrix_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_matrix.jpg'), D * 255)
        scipy.misc.imsave(os.path.join(matrix_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_enhance.jpg'), DD * 255)
        
        ## Save matching 
        match = getMatches(DD, 0, args)
        m = match[:,0]
        thresh = 0.95
        matched = match[match[:,1]<thresh, 1]
        score = np.mean(matched)
        m[match[:,1] > thresh] = np.nan
        plt.figure()
        plt.xlabel('Test data')
        plt.ylabel('Stored data')
        plt.text(60, .025, r"score=%4.4f, point=%d" % (score, len(matched)))
        plt.plot(m,'.') 
        plt.title('Epoch_'+img_epoch+'_'+pcd_epoch+'_'+file_name)
        plt.savefig(os.path.join(match_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_match.jpg'))
        plt.close()

        ## Caculate Precision and Recall Curve
        np.set_printoptions(threshold='nan')
        match_PR = match[int(args.v_ds/2):int(match.shape[0]-args.v_ds/2), :]
        for match_id in range(len(match_PR)):
            train_id = int(match_PR[match_id, 0])
            test_id  = match_id+int(int(args.v_ds/2))
            distance = np.linalg.norm(train_pose[train_id]-test_pose[test_id])

            if distance <= args.match_distance:
                match_PR[match_id,0] = 1
            else:
                match_PR[match_id,0] = 0

        #print (match_PR)
        match_PR[np.isnan(match_PR)]=0
        match_path = os.path.join(pr_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_match.json')
        with open(match_path, 'w') as data_out:
            json.dump(match_PR.tolist(), data_out)

        precision, recall, _ = precision_recall_curve(match_PR[:, 0], match_PR[:, 1])
        PR_data = zip(precision, recall) 
        PR_path = os.path.join(pr_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_PR.json')
        with open(PR_path, 'w') as data_out:
            json.dump(PR_data, data_out)
            
        fpr, tpr, _ = roc_curve(match_PR[:, 0], match_PR[:, 1])
        roc_auc     = auc(fpr, tpr)
        
        ROC_data = zip(fpr, tpr) 
        ROC_path = os.path.join(pr_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_ROC.json')
        with open(ROC_path, 'w') as data_out:
            json.dump(ROC_data, data_out)

        plt.figure()
        plt.xlim(0.0, 1.0)
        plt.ylim(0.0, 1.0)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.plot(recall, precision, lw=2, color='navy', label='Precision-Recall curve')
        plt.plot(fpr, tpr, lw=2, color='deeppink', label='ROC curve')
        plt.title('PR Curve for Epoch_'+img_epoch+'_'+pcd_epoch+'_'+file_name+'  (area={0:0.2f})'.format(roc_auc))
        plt.savefig(os.path.join(pr_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_PR.jpg'))
        plt.close()

        ## Save sub enhance
        plt.figure()
        fig, ax = plt.subplots()
        ax.imshow(DD_sub, cmap=plt.cm.gray, interpolation='nearest')
        #ax.set_title('Enhance Matrix')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.savefig(os.path.join(matrix_dir, img_epoch+'_'+pcd_epoch+'_'+file_name+'_sub_enhance.jpg'))
        plt.close()
