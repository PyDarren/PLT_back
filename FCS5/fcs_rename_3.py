from FCS import Fcs
from tkinter import filedialog
import os
import re
from tkinter import Tk

# 选择路径
root = Tk()
root.withdraw()
Fpath = filedialog.askdirectory()

# 读取panel表信息
panel_file = Fpath + "/panel.xlsx"
panel_tuple = Fcs.export_panel_tuple(panel_file)
print(panel_tuple)

for filename in [filename for filename in os.listdir(Fpath) if os.path.splitext(filename)[1] == ".fcs"]:
    file = Fpath + '/' + filename
    fcs = Fcs(file)


    pars = fcs.delete_channel(fcs.pars, 89, 115, 140, 115)
    # pars = fcs.marker_rename(fcs.pars, *panel_tuple)
    # stain_channel_index = fcs.get_stain_channels(pars)
    #
    # # 添加event_length, 191, 193, 194, 140
    # add_channel = ["Event_length", "Ir191Di", "Ir193Di", "Pt194Di", "Ce140Di"]
    # add_index = [i + 1 for i in range(0, len(pars)) if pars[i].par_short_name in add_channel]
    # stain_channel_index.extend(add_index)
    # pars = [pars[i] for i in range(0, len(pars)) if i + 1 in stain_channel_index]

    # 根据当前的filename去查找新的name
    new_filename = re.sub("-", "", filename)
    # new_filename = re.sub("^.+?_", "gsH_", new_filename)
    new_file = Fpath + "/WriteFcs/" + new_filename

    fcs.write_to(new_file, pars)
