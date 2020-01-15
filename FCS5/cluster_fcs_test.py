from FCS import *
from tkinter import filedialog
import os
from tkinter import Tk

# 选择路径
root = Tk()
root.withdraw()
Fpath = filedialog.askdirectory()
# print(Fpath)
"C:/Users/PC/Desktop/cluster_fcs_test/spade"
"C:/Users/PC/Desktop/cluster_fcs_test/spade_anno"
"C:/Users/PC/Desktop/cluster_fcs_test/xshift"


file_tuple = tuple([Fpath + '/' + filename for filename in os.listdir(Fpath)
                    if os.path.splitext(filename)[1] == ".fcs"])

fcs = ClusterFcs(file_tuple[0])
print([par.par_name for par in fcs.pars])
print(fcs.pars[len(fcs.pars)-1].data[0:100])

temp = sys.stdout
# 运行记录打印到指定文件中
sys.stdout = open(Fpath + '/log.txt', 'a')
file = Fpath + "/MergeFcs/test.fcs"
merge_fcs(file, *file_tuple)

sys.stdout = temp

for filename in [filename for filename in os.listdir(Fpath) if os.path.splitext(filename)[1] == ".fcs"]:
    file = Fpath + '/' + filename
    fcs = Fcs(file)

    pars = fcs.pars
    # # 降采样
    # pars = fcs.down_sample(pars, 50000)
    # # 重命名
    # pars = fcs.marker_rename(pars, (115, "CD3_test"), (89, "cd45_test"))

    # 删除通道
    pars = fcs.delete_channel(pars, 166)

    # 根据当前的filename去查找新的name
    new_file = Fpath + "/newfcs/" + filename
    fcs.write_to(new_file, pars)







