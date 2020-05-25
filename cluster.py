import numpy as np
from pandas import Series

def threshold_cluster(Data_set,threshold):
    stand_array=np.asarray(Data_set).ravel('C')
    stand_Data=Series(stand_array)
    index_list,class_k=[],[]
    while stand_Data.any():
        if len(stand_Data)==1:
            index_list.append(list(stand_Data.index))
            class_k.append(list(stand_Data))
            stand_Data=stand_Data.drop(stand_Data.index)
        else:
            class_data_index=stand_Data.index[0]
            class_data=stand_Data[class_data_index]
            stand_Data=stand_Data.drop(class_data_index)
            if (abs(stand_Data-class_data)<=threshold).any():
                args_data=stand_Data[abs(stand_Data-class_data)<=threshold]
                stand_Data=stand_Data.drop(args_data.index)
                index_list.append([class_data_index]+list(args_data.index))
                class_k.append([class_data]+list(args_data))
            else:
                index_list.append([class_data_index])
                class_k.append([class_data])
    return index_list,class_k

if __name__ == "__main__":
    Data_set = [1, 1.1, 0.9, -5, 2, 100, 99, -4.2, 10000, 0]
    index_list, class_k = threshold_cluster(Data_set, 5)
    print index_list, class_k