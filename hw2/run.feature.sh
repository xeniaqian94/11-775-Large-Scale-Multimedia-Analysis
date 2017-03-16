
cluster_num=1000
#python select_frame.py list/train_dev.video 0.1 selected_sift
for cluster_num in 500 1000; do
#python train_kmeans.py selected_sift ${cluster_num} model/sift.kmeans.${cluster_num}.model
echo ${cluster_num} " train model finished!"
python create_kmeans.py model/sift.kmeans.${cluster_num}.model ${cluster_num} list/all.video ../sift_feature_${cluster_num}/


done
