"""
读取fcs文件
The parameter description keywords (e.g. $PnR, $PnB, etc) are numbered consecutively in the
order in which the parameters are written to the file, beginning with number 1. The required and
optional FCS keywords are listed below with one line descriptions. The keywords and their values
are described in alphabetical order following the lists. Required keywords are so indicated.

Values of numerical keywords (e.g., values of $BEGINANALYSIS, $BEGINDATA,
$BEGINSTEXT, $ENDANALYSIS, $ENDDATA, $ENDSTEXT, $NEXTDATA, $PAR, $PnB,
$PnR, $TOT) shall not be padded with any non-numerical characters (including spaces and other
white characters). However, leading zeros '0' (ASCII 48) may be used. For example, you may use
$BEGINDATA/0000012345/ and you may not use $BEGINDATA/ 12345/.

The required FCS primary TEXT segment keywords are as follows:
$BEGINANALYSIS Byte-offset to the beginning of the ANALYSIS segment.
$BEGINDATA Byte-offset to the beginning of the DATA segment.
$BEGINSTEXT Byte-offset to the beginning of a supplemental TEXT segment.
$BYTEORD Byte order for data acquisition computer.
$DATATYPE Type of data in DATA segment (ASCII, integer, floating point).
$ENDANALYSIS Byte-offset to the last byte of the ANALYSIS segment.
$ENDDATA Byte-offset to the last byte of the DATA segment.
$ENDSTEXT Byte-offset to the last byte of a supplemental TEXT segment.
$MODE Data mode (list mode - preferred, histogram - deprecated).
$NEXTDATA Byte offset to next data set in the file.
$PAR Number of parameters in an event.
$PnB Number of bits reserved for parameter number n.
$PnE Amplification type for parameter n.
$PnN Short name for parameter n.
$PnR Range for parameter number n.
$TOT Total number of events in the data set.

The optional FCS TEXT segment keywords are as follows:
$ABRT Events lost due to data acquisition electronic coincidence.
$BTIM Clock time at beginning of data acquisition.
$CELLS Description of objects measured.
$COM Comment.
$CSMODE Cell subset mode, number of subsets to which an object may belong.
$CSVBITS Number of bits used to encode a cell subset identifier.
$CSVnFLAG The bit set as a flag for subset n.
$CYT Type of flow cytometer.
$CYTSN Flow cytometer serial number.
$DATE Date of data set acquisition.
$ETIM Clock time at end of data acquisition.
$EXP Name of investigator initiating the experiment.
$FIL Name of the data file containing the data set.
$GATE Number of gating parameters.
$GATING Specifies region combinations used for gating.
$GnE Amplification type for gating parameter number n (deprecated).
$GnF Optical filter used for gating parameter number n (deprecated).
$GnN Name of gating parameter number n (deprecated).
$GnP Percent of emitted light collected by gating parameter n (deprecated).
$GnR Range of gating parameter n (deprecated).
$GnS Name used for gating parameter n (deprecated).
$GnT Detector type for gating parameter n (deprecated).
$GnV Detector voltage for gating parameter n (deprecated).
$INST Institution at which data was acquired.
$LAST_MODIFIED Timestamp of the last modification of the data set.
$LAST_MODIFIER Name of the person performing last modification of a data set.
$LOST Number of events lost due to computer busy.
$OP Name of flow cytometry operator.
$ORIGINALITY Information whether the FCS data set has been modified (any part of it)
or is original as acquired by the instrument.
$PKn Peak channel number of univariate histogram for parameter n
(deprecated).
$PKNn Count in peak channel of univariate histogram for parameter n
(deprecated).
$PLATEID Plate identifier.
$PLATENAME Plate name.
$PnCALIBRATION Conversion of parameter values to any well defined units, e.g., MESF.
$PnD Suggested visualization scale for parameter n.
$PnF Name of optical filter for parameter n.
$PnG Amplifier gain used for acquisition of parameter n.
$PnL Excitation wavelength(s) for parameter n.
$PnO Excitation power for parameter n.
$PnP Percent of emitted light collected by parameter n.
$PnS Name used for parameter n.
$PnT Detector type for parameter n.
$PnV Detector voltage for parameter n.
$PROJ Name of the experiment project.
$RnI Gating region for parameter number n.
$RnW Window settings for gating region n.
$SMNO Specimen (e.g., tube) label.
$SPILLOVER Fluorescence spillover matrix.
$SRC Source of the specimen (patient name, cell types)
$SYS Type of computer and its operating system.
$TIMESTEP Time step for time parameter.
$TR Trigger parameter and its threshold.
$VOL Volume of sample run during data acquisition.
$WELLID Well identifier.

fcs文件二进制格式
$DATATYPE/c/ $DATATYPE/I/ [REQUIRED]
This keyword describes the type of data written in the DATA segment of the data set. The four
allowed values are 'I', 'F', 'D', or 'A'. The DATA segment is a continuous bit stream with no
delimiters. 'I' stands for unsigned binary integer, F stands for single precision IEEE floating point,
'D' stands for double precision IEEE floating point, and 'A' stands for ASCII. The additional
keywords $PnB (bits per parameter) and $PnR (range per parameter) are needed to completely
describe an event in the DATA segment.
$DATATYPE/I/ means that the events are written as unsigned binary integers. For each
parameter in an event, both the maximum length in bits allocated for storage of the parameter
and the actual integer range used by the parameter within that allocation are needed. The
number of bits per parameter is specified by $PnB. For example, $P1B/16/ specifies that 16 bits
are allocated for parameter 1. $P1R/1024/ specifies that parameter 1 values range from 0 to
1023. This allows the data word length to be specified, facilitating compatibility between machines
with different data word lengths and enabling bit compression of the data.
$DATATYPE/F/ means that the data are written as single precision floating point values in the
IEEE standard format (5). Note that the $PnB keywords should be set to a value of 32 for each
parameter in an event. For example, $P1B/32/. In this case, the value of the $P1R keyword
represents the original resolution to acquire the data; however, it may not correspond to the range
where data is stored. Note that $PnE/0,0/ shall be used for all parameters if $DATATYPE/F/ is
used.
$DATATYPE/D/ means that the data are written as double precision floating point values in the
IEEE standard format (5). The $PnB keyword should be set to a value of 64 for each parameter in
an event. For example, $P3B/64/ says that parameter 3 is allocated 64 bits of storage space. In
this case, the value of the $P1R keyword represents the original resolution to acquire the data;
however, it may not correspond to the range where data is stored. Note that $PnE/0,0/ shall be
used for all parameters if $DATATYPE/D/ is used.
$DATATYPE/A/ is deprecated in FCS 3.1. While still allowed, the users are discouraged from
using $DATATYPE/A/ as it will likely not be supported by future revisions of the FCS standard.
$DATATYPE/A/ means that the data are written as ASCII-encoded integer values. In this case,
the keyword $PnB specifies the number of bytes allocated per value (one byte per character).
This represents fixed format ASCII data. $P1B/4/ indicates that the maximum value for parameter
1 would be 9999. Data are stored in a continuous byte stream, with no delimiters. If the value of
the $PnB keyword is the * character, e.g., $P1B/*/, the data are free format and number of
characters per parameter value may vary. In this case, all values are separated by one of the
following delimiters: "space", "tab", "comma", "carriage return", or "line feed" characters. Note that
multiple, consecutive delimiters are treated as a single delimiter. Since there are significant
differences between the ways in which consecutive delimiters are treated by different
programming languages, care should be taken when using this format. Zero values must be
explicitly specified by the "0" (ASCII 48) character. Thus, the string "1,3,, ,3" (note the space
between the third and fourth commas) would only specify three values.
"""
import sys
import struct
import datetime
import re
import xlrd
import os
import pandas as pd
import numpy as np
import copy


def check_list_equally(my_list):
    my_list = [element for element in my_list if element is not None]
    iterator = iter(my_list)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)


def check_channel_equally(*args):
    """
    检查fcs文件之间是否通道/染色通道一致
    传进多个fcs文件名称
    """
    if len(args) == 1:
        print("只有一个fcs，无需检查通道一致！")
        return

    pars_list = [Fcs(file).pars for file in args]

    same_channel_index = []
    # 检查通道数量是否一致
    print("检查通道数量是否一致？")

    channel_num_list = [len(pars) for pars in pars_list]
    channel_num_equally = check_list_equally(channel_num_list)
    marker_name_equally = False

    if channel_num_equally:
        print("所有fcs文件通道数量一致！")
    else:
        for num in set(channel_num_list):
            file_name = [args[i].split("/")[-1] for i in range(0, len(channel_num_list)) if channel_num_list[i] == num]
            print("通道数量为%d文件有:%s" % (num, "; ".join(file_name)))
        return pars_list, same_channel_index, channel_num_equally, marker_name_equally

    # 检查每个通道上的marker是否一致
    print("检查marker名称是否一致？")

    channel_num = channel_num_list[0]
    for channel_index in range(0, channel_num):
        # channel_short_name = [pars[channel_index].par_short_name for pars in pars_list]
        channel_name = [pars[channel_index].par_name for pars in pars_list]
        # 如果当前marker的名字在所有fcs文件中不一致，打印出来
        if check_list_equally(channel_name) is not True:
            for name in set(channel_name):
                file_name = [args[i].split("/")[-1] for i in range(0, len(channel_name)) if
                             channel_name[i] == name]
                print("maker名为%s文件有:%s" % (name, "; ".join(file_name)))
            print("")
        # 如果maker名在所有fcs上一致,记录此通道索引
        else:
            same_channel_index.append(channel_index)

    marker_name_equally = len(same_channel_index) == channel_num
    if marker_name_equally:
        print("所有fcs文件marker名称一致！")

    return pars_list, same_channel_index,  channel_num_equally, marker_name_equally


def rename_by_panel_table(panel_table, *args):
    """
    根据panel表，修改fcs文件marker name
    传进多个fcs文件名称
    传进的panel_table是一个嵌套元组，如((115, CD3), (89, cd45))
    """
    # 检查传进来的fcs文件通道数量是否一致
    pars_list, same_channel_index, channel_num_equally, marker_name_equally = check_channel_equally(*args)
    if channel_num_equally is not True:
        print("FCS文件通道数量不一致！！！")
        return

    for i in range(0, len(pars_list)):
        pars = pars_list[i]
        file = args[i]
        # 传入的是嵌套元组
        pars = Fcs.marker_rename(pars, *panel_table)  # 传入panel表中的（通道名字，marker名字）

        save_dir = "/".join(file.split("/")[0:-1]) + "/rename_by_panelTable/"
        new_file = save_dir + file.split("/")[-1]
        Fcs.write_to(new_file, pars)


def merge_fcs(file, *args):
    """
    合并fcs文件
    传进多个fcs文件名称
    """
    if len(args) == 1:
        print("只有一个fcs，无需合并！")
        return

    # 检查传进来的fcs文件是否一致
    pars_list, same_channel_index, channel_num_equally, marker_name_equally = check_channel_equally(*args)
    if channel_num_equally & marker_name_equally is not True:
        print("无法 merge！！！")
        return

    # 合并pars的data
    merge_pars = pars_list[0]
    channel_num = len(merge_pars)
    for i in range(1, len(pars_list)):
        pars = pars_list[i]
        for p in range(0, channel_num):
            merge_pars[p].data = merge_pars[p].data + pars[p].data

    # 对新组合成的data顺序重新打乱，随机排序
    event_num = len(merge_pars[0].data)
    new_index = np.random.choice(np.r_[0:event_num], event_num, replace=False)
    for par in merge_pars:
        par.data = [par.data[i] for i in new_index]

    # 写出到fcs中
    channel_name = [par.par_short_name for par in merge_pars]
    marker_name = [par.par_name for par in merge_pars]
    data = [par.data for par in merge_pars]
    Write(file, channel_name, marker_name, data)
    print("%s 合并完成！" % file)


class Parameter(object):
    """
    每个通道一般都包含一下几个参数信息
    $PnN Short name for parameter n.
    $PnS Name used for parameter n.
    $PnR Range for parameter number n.
    $PnB Number of bits reserved for parameter number n.
    $PnE Amplification type for parameter n.
    """
    # 限定Parameter对象只能绑定par_short_name($PnN), par_name($PnS),
    # par_range($PnR), par_bits($PnB), par_amp($PnE)等属性
    __slots__ = ("par_short_name", "par_name", "par_range", "par_bits", "par_amp",
                 "nb_bytes", "fmt", "data")

    def __init__(self, par_short_name, par_name, par_range, par_bits, par_amp, nb_bytes, fmt, data):
        self.par_short_name = par_short_name
        self.par_name = par_name
        self.par_range = par_range
        self.par_bits = par_bits
        self.par_amp = par_amp
        self.nb_bytes = nb_bytes
        self.fmt = fmt  # unpack模式
        self.data = data


class Fcs(object):
    panel_tuple = None

    def __init__(self, file):
        """
        fcs文件属性，主要由header_bef, header, pars三个部分构成
        """
        self.file_dir = "/".join(file.split('/')[0:-1])
        self.file_name = file.split('/')[-1]

        self.position = {}
        self.info = {}
        self.pars = []
        with open(file, 'rb') as f:
            self.__is_fcs_file(f)
            self.__get_position(f)
            self.__get_info(f)
            self.__get_pars()
            self.__get_data(f)
        self.stain_channels_index = self.get_stain_channels(self.pars)
        self.preprocess_channels_index = self.get_preprocess_channels(self.pars)

    def __is_fcs_file(self, f):
        """
        判断是否是一个fcs3.0文件
        """
        # fcs文件的格式，一般是3.0, 如果不是fcs3.0，抛出异常
        f.seek(0)
        file_format = str(f.read(6), encoding="utf-8")
        try:
            if file_format == "FCS3.0":
                # print("%s 是FCS3.0文件" % self.filename)
                return
            else:
                file_format_error = Exception(self.file_name + "不是一个FCS3.0的文件")
                raise file_format_error
        except Exception as result:
            sys.stderr.write(str(result)+"\n")

    def __get_position(self, f):
        """
        获取fcs文件中，head中的起始和结束位置，data起始和结束位置，analysis起始和结束位置
        """
        f.seek(10)
        # head的起始位置和终止位置
        self.position["head_start"] = int(str(f.read(8), encoding="utf-8").strip(" "))
        self.position["head_end"] = int(str(f.read(8), encoding="utf-8").strip(" "))
        # 数据的起始位置和终止位置
        self.position["data_start"] = int(str(f.read(8), encoding="utf-8").strip(" "))
        self.position["data_end"] = int(str(f.read(8), encoding="utf-8").strip(" "))
        # 分析的起始位置和终止位置
        self.position["analysis_start"] = int(str(f.read(8), encoding="utf-8").strip(" "))
        self.position["analysis_end"] = int(str(f.read(8), encoding="utf-8").strip(" "))

    def __get_info(self, f):
        """
        获取fcs文件中的txt部分中的信息, 把txt部分分割，生成info字典
        """
        # 定位到header起始位置
        f.seek(self.position["head_start"])
        # 如果txt中的文件路径包含中文，用GB2312解码, 中文用两个字节表示一个字符
        # utf-8编码把存储英文依旧用一个字节，汉字就3个字节
        bin_txt_str = f.read(self.position["head_end"] + 1 - self.position["head_start"])
        try:
            txt_str = str(bin_txt_str, encoding="utf-8")
        except UnicodeDecodeError:
            print("%s文件保存路径中可能包含中文路径！不要使用中文路径！！！" % self.file_name)
            txt_str = str(bin_txt_str, encoding="GB2312")

        # 获取分隔符
        sep = txt_str[0]
        fields = txt_str.split(sep)
        fields.pop(0)  # 去除分割产生的第一个空字符串
        fields.pop(-1)  # 去除分割产生的最后一个空字符串
        # 使用列表推导式分别获得key和对应的值
        key = [fields[i].upper() for i in range(0, len(fields)) if i % 2 == 0]
        val = [fields[i] for i in range(0, len(fields)) if i % 2 == 1]
        # 使用字典推导式获得info
        self.info = {key[i]: val[i] for i in range(0, len(key))}

        # 判断header中data位置与txt中$BEGINDATA，$ENDDATA是否一致
        if "$BEGINDATA" in self.info.keys()and self.position["data_start"] != self.info["$BEGINDATA"]:
            self.position["data_start"] = max(self.position["data_start"], int(self.info["$BEGINDATA"]))
        if "$ENDDATA" in self.info.keys()and self.position["data_end"] != self.info["$ENDDATA"]:
            self.position["data_end"] = max(self.position["data_end"], int(self.info["$ENDDATA"]))

        # 判断是否带有补偿矩阵
        if "$SPILLOVER" in self.info.keys():
            print("The File has compensation Matrix!")

        # 判断analysis部分是否不为空
        if self.info["$NEXTDATA"] in self.info.keys() and self.info["$NEXTDATA"] != "0":
            sys.stderr.write("Some other data exist in the file but hasn't been parsed.\n")

        print("%s events were detected; Each event is characterized by %s parameters" %
              (self.info["$TOT"], self.info["$PAR"]))

    def __get_pars(self):
        """
        每个通道一般都包含一下几个参数信息
        $PnN Short name for parameter n.
        $PnS Name used for parameter n.
        $PnR Range for parameter number n.
        $PnB Number of bits reserved for parameter number n.
        $PnE Amplification type for parameter n.
         DATATYPE
         I stands for unsigned binary integer I
         F stands for single precision IEEE floating point 单精度浮点数 f
         D stands for double precision IEEE floating point 双精度浮点数 d
         A stands for ASCII
         The additional keywords $PnB (bits per parameter) and $PnR (range per parameter) are needed to completely
         describe an event in the DATA segment.
        """
        # 字节顺序
        if self.info["$BYTEORD"] == "4,3,2,1":
            endianness = ">"
        else:
            endianness = "<"
            assert self.info["$BYTEORD"] == "1,2,3,4"

        if self.info["$DATATYPE"] != "F":
            raise NotImplementedError

        for i in range(1, int(self.info["$PAR"]) + 1):
            par_short_name = self.info["$P%dN" % i] if "$P"+str(i)+"N" in self.info else None
            par_name = self.info["$P%dS" % i] if "$P"+str(i)+"S" in self.info else None
            par_range = self.info["$P%dR" % i] if "$P"+str(i)+"R" in self.info else None
            par_bits = self.info["$P%dB" % i]
            par_amp = self.info["$P%dE" % i] if "$P"+str(i)+"E" in self.info else None

            nb_bits = int(par_bits)
            assert nb_bits % 8 == 0
            nb_bytes = nb_bits / 8
            if nb_bytes == 1:
                c_type = "B"  # unsigned char
            elif nb_bytes == 2:
                c_type = "H"  # unsigned short
            elif nb_bytes == 4:
                c_type = "f"  # precision IEEE floating point
            elif nb_bytes == 8:
                c_type = "d"  # double precision IEEE floating point
            else:
                raise ValueError("不是有效的Bit整数")
            fmt = endianness + c_type  # unpack模式
            data = []

            par = Parameter(par_short_name, par_name, par_range, par_bits, par_amp, nb_bytes, fmt, data)
            self.pars.append(par)

    def __get_data(self, f):
        """
        fcs_data得到的是字节Byte形式存储的,数据存储以字节为单位，数据传输通常以位bit为单位，通常一字节是8位bit
        """
        row_bytes = sum([par.nb_bytes for par in self.pars])
        row_fmt = ">" + re.sub(">", "", ''.join([par.fmt for par in self.pars]))
        event_num = int(self.info["$TOT"])
        par_num = int(self.info["$PAR"])

        # unpack data
        t_start = datetime.datetime.now()
        f.seek(self.position["data_start"])
        for row in range(0, event_num):
            # 一行二进制数据根据每个通道的存储字节来转换成常规数值
            row_values = struct.unpack(row_fmt, f.read(int(row_bytes)))
            [self.pars[i].data.append(row_values[i]) for i in range(0, par_num)]
        t_end = datetime.datetime.now()
        print("read %s elapse %s" % (self.file_name, (t_end - t_start)))

    @ staticmethod
    def get_stain_channels(pars):
        """
        找出染色的通道，返回染色通道的索引
        """
        stain_channels_index = []
        for i in range(0, len(pars)):
            channel_name = pars[i].par_name
            if channel_name is None:
                continue
            # 判断channel_name是否是 数字+字母+_marker的模式
            elif re.match(r"\d+.+_", channel_name):
                # 判断channel_name中是否包含DNA|cisplatin|barcode字符
                if re.search("DNA|cisplatin|barcode", channel_name):
                    continue
                else:
                    stain_channels_index.append(i+1)
        return stain_channels_index

    @ staticmethod
    def get_preprocess_channels(pars):
        """
        找出包含预处理的通道，返回找到的通道的索引
        """
        # 根据通道名字，添加event_length， 191， 193， 194, 140
        # 根据marker名字, 添加 Event_length, DNA1, DNA2, cisplatin, beads
        add_channel = ["Event_length", "Ir191Di", "Ir193Di", "Pt194Di", "Ce140Di"]
        add_marker = ["Event_length", "DNA1", "DNA2", "cisplatin", "beads"]

        preprocess_channels_index = []
        for i in range(0, len(pars)):
            channel_name = pars[i].par_short_name
            marker_name = re.sub(r"^.+?_", "", pars[i].par_name) if pars[i].par_name is not None else ""
            if channel_name in add_channel and marker_name in add_marker:
                preprocess_channels_index.append(i+1)
            elif marker_name == "cisplatin":
                preprocess_channels_index.append(i + 1)
            elif channel_name == "Ce140Di":
                preprocess_channels_index.append(i + 1)
            elif channel_name == "Event_length":
                preprocess_channels_index.append(i + 1)

        return preprocess_channels_index

    @staticmethod
    def write_to(file, pars, to="fcs"):
        """
        将pars文件信息写出到csv中或fcs中
        默认写入到fcs文件中
        """
        if to == "csv":
            # 写入抬头信息
            marker_name = [re.sub("^.+?_", "", par.par_name) if par.par_name is not None else par.par_short_name
                           for par in pars]
            marker_name = [marker_name[i] if marker_name[i] != "" else pars[i].par_short_name for i in
                           range(0, len(pars))]

            data = [par.data for par in pars]
            df = pd.DataFrame(data).T
            df.columns = marker_name
            df.to_csv(file, index=False)
        elif to == "fcs":
            channel_name = [par.par_short_name for par in pars]
            marker_name = [par.par_name for par in pars]
            data = [par.data for par in pars]
            Write(file, channel_name, marker_name, data)

    @staticmethod
    def delete_channel(pars, *args):
        """
        删除指定通道，传入进来的可以是通道数字，如89， 103， 104，或者是通道完整名字
        写到fcs文件中
        """
        channel_name_1 = [par.par_short_name for par in pars]
        channel_name_2 = [re.sub(r"[^\d+]", "", name) for name in channel_name_1]
        # 查找要删除的通道的索引
        delete_channel_index = []
        for tmp_arg in args:
            tmp_arg = str(tmp_arg)
            try:
                index = channel_name_1.index(tmp_arg)
                delete_channel_index.append(index)
            except ValueError:
                index = channel_name_2.index(tmp_arg)
                delete_channel_index.append(index)
        # 删除pars中对应的通道
        pars = [pars[i] for i in range(0, len(pars)) if i not in delete_channel_index]
        return pars

    @staticmethod
    def export_channel(pars, *args):
        """
        导出指定通道，传入进来的可以是通道数字，如89， 103， 104，或者是通道完整名字
        写到fcs文件中
        """
        channel_name_1 = [par.par_short_name for par in pars]
        channel_name_2 = [re.sub(r"[^\d+]", "", name) for name in channel_name_1]
        # 查找要导出的通道的索引
        export_channel_index = []
        for tmp_arg in args:
            tmp_arg = str(tmp_arg)
            try:
                index = channel_name_1.index(tmp_arg)
                export_channel_index.append(index)
            except ValueError:
                index = channel_name_2.index(tmp_arg)
                export_channel_index.append(index)
        # 删除pars中对应的通道
        pars = [pars[i] for i in range(0, len(pars)) if i in export_channel_index]
        return pars

    @staticmethod
    def add_channel(pars, *args):
        """
        往数据中添加一个通道及数据, 传进来的是(（channel_name, marker_name, data）, （channel_name, marker_name, data）)形式
        """
        # 默认在末尾添加
        for tmp_arg in args:
            par_short_name = tmp_arg[0]
            par_name = tmp_arg[1]
            data = tmp_arg[2]
            # 其他信息复制原有第一个通道中的信息
            par_range = max(tmp_arg[2])
            par_bits = pars[0].par_bits
            par_amp = pars[0].par_bits
            nb_bytes = pars[0].par_bits
            fmt = pars[0].par_bits

            par = Parameter(par_short_name, par_name, par_range, par_bits, par_amp, nb_bytes, fmt, data)
            pars.append(par)
        return pars

    @staticmethod
    def marker_rename(pars, *args):
        """
        修改marker_name,传入如(115，"CD3"), (89, "cd45), 或(通道完整名字，marker名字)
        """
        channel_name_1 = [par.par_short_name for par in pars]
        channel_name_2 = [re.sub(r"[^\d+]", "", name) for name in channel_name_1]
        # 查找要修改marker名称的通道的索引
        for tmp_arg in args:
            tmp_rename_channel = str(tmp_arg[0])
            try:
                index = channel_name_1.index(tmp_rename_channel)
            except ValueError:
                index = channel_name_2.index(tmp_rename_channel)
            # 修改marker name
            marker_name = pars[index].par_name
            marker_name = '_'.join([marker_name.split("_")[0], tmp_arg[1]]) if marker_name is not None else tmp_arg[1]
            pars[index].par_name = marker_name
        return pars

    @staticmethod
    def down_sample(pars, *args):
        """
        对数据进行降采样
        可以传入要降采样的数目或者要降采样的行的索引
        """
        down_sample_index = []
        event_num = len(pars[0].data)
        if len(args) == 1:
            down_sample_num = int(args[0])
            # 判断down_sample_num是否超过原有行数
            if down_sample_num >= event_num:
                return pars
            elif down_sample_num < event_num:
                # 随机抽取指定数目的行数, 无放回抽样
                down_sample_index = list(np.random.choice(np.r_[0:event_num], down_sample_num, replace=False))
        elif len(args) >= 1:
            down_sample_index = list(args)

        for par in pars:
            par.data = [par.data[i] for i in down_sample_index]

        return pars

    @classmethod
    def export_panel_tuple(cls, panel_file):
        """
        根据传进来的panel表文件，生成panel_tuple, panel_tuple是一个嵌套元组，如((115, CD3), (89, cd45))
        :param panel_file:
        :return: panel_tuple
        """
        print("")
        print("读取panel表")
        # 读取panel表信息
        workbook = xlrd.open_workbook(panel_file)
        panel_sheet = workbook.sheet_by_name('panel')

        channel = panel_sheet.col_values(0)
        channel = [re.sub(r"[^\d+]", "", tmp_channel) if tmp_channel.isalnum() else tmp_channel
                   for tmp_channel in channel]

        marker = panel_sheet.col_values(1)
        marker = [re.sub("（", "(", tmp_marker) for tmp_marker in marker]
        marker = [re.sub("）", ")", tmp_marker) for tmp_marker in marker]

        if len(channel) == len(marker):
            cls.panel_tuple = tuple([(channel[i], marker[i]) for i in range(0, len(channel))])
        else:
            print("panel表中的channel和marker数量不一致！！！")

        return cls.panel_tuple


class StainFcs(Fcs):
    def __init__(self, file):
        super().__init__(file)
        # 删除pars中对应的通道
        # 先判断有没有染色通道
        if len(self.stain_channels_index) != 0:
            self.pars = [self.pars[i] for i in range(0, len(self.pars)) if i+1 in self.stain_channels_index]
        else:
            print("所有通道都没有染色!!!")
            assert len(self.stain_channels_index) == 0


class ClusterFcs(Fcs):
    def __init__(self, file):
        super().__init__(file)
        # 找出通道名称中带有cluster的通道
        self.cluster_channel_index = [i for i in range(0, len(self.pars))
                                      if re.match("cluster", self.pars[i].par_short_name, flags=re.IGNORECASE)][0]

    def __edit_raw_cluster_id(self):
        # 对原始的cluster_id重大到小排序
        # 因为x-shift的聚类原始id数值比较大
        cluster_id = np.unique(self.pars[self.cluster_channel_index].data)


    """
    1. 改cluster-id
    2. 合并cluster-id
    """


    def cluster_method(self):



        """
        sapde 聚类算法未做注释，会增加一列，cluster-assign
        sapde 聚类算法做过注释，会增加两列，cluster-assign和annotation
        xshif聚类算法，会增加一列，如clusterID X-shift (Gradient assignment),  K=100
        """


        # 修改聚类通道名称为 Cluster_ID
        self.pars[cluster_channel_index].par_name = "Cluster_ID"
        self.pars[cluster_channel_index].par_short_name = "Cluster_ID"

        if len(self.pars) - cluster_channel_index == 2:
            # 如果有annotation这一列
            self.pars[cluster_channel_index + 1].par_name = "Annotation"
            self.pars[cluster_channel_index + 1].par_short_name = "Annotation"
        elif len(self.pars) - cluster_channel_index == 1:
            # 如果没有有annotation这一列，将cluster的通道作为Annotation通道
            annotation_channel = copy.deepcopy(self.pars[cluster_channel_index])
            annotation_channel.par_name = "Annotation"
            annotation_channel.par_short_name = "Annotation"
            self.pars.insert(cluster_channel_index + 1, annotation_channel)


class Write(object):
    def __init__(self, file, channel_name, marker_name, data):
        # 传入的filename是一个绝对路径
        self.file = file
        self.channel_name = channel_name
        self.marker_name = marker_name
        self.data = data
        self.__check_length()
        self.info = self.__export_info()

        # 查看是否存在file中包含得路径
        save_dir = "/".join(self.file.split("/")[0:-1])
        # excel文件夹不存在时创建
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(self.file, 'wb') as f:
            self.__write_header_txt(f)
            self.__write_data(f)

    def __check_length(self):
        data_length_set = {len(tmp_data) for tmp_data in self.data}
        if len(data_length_set) != 1:
            print("传入的通道数据长度不一致！！！")
            assert len(data_length_set) == 1

        if len({len(self.channel_name), len(self.marker_name), len(self.data)}) != 1:
            print("传入的通道和marker, data数量不一致！！！")
            print("通道数量：%d, marker数量：%d, data数量：%d" % (len(self.channel_name), len(self.marker_name), len(self.data)))
            assert {len(self.channel_name), len(self.marker_name), len(self.data)} == 1

    def __export_info(self):
        """
        组装出fcs文件的txt信息
        """
        info = {}
        filename = self.file.split("/")[-1]
        info["FILENAME"] = filename
        info["$FIL"] = filename
        info["CREATOR"] = "PLT"
        info["$CYT"] = "DVSSCIENCES-CYTOF"
        info["FCSVERSION"] = "3"
        info["FJ_FCS_VERSION"] = "3"
        info["$DATATYPE"] = "F"
        info["$MODE"] = "L"
        info["$BYTEORD"] = "4,3,2,1"

        channel_num = len(self.channel_name)
        event_num = len(self.data[0])
        data_bytes = channel_num * event_num * 4
        # 默认写出的数据位置从5000开始,前5000位放header+txt
        data_start = 5000
        data_end = data_bytes + data_start - 1
        info["$BEGINSTEXT"] = str("0")
        info["$ENDSTEXT"] = str("0")
        info["$BEGINDATA"] = str(data_start)
        info["$ENDDATA"] = str(data_end)
        info["$BEGINANALYSIS"] = str("0")
        info["$ENDANALYSIS"] = str("0")
        info["$NEXTDATA"] = str("0")

        info["ORIGINALGUID"] = "1.fcs"
        info["GUID"] = "1.fcs"

        info["$PAR"] = str(channel_num)
        info["$TOT"] = str(event_num)

        """
        主要通道类别
        $PnN Short name for parameter n.
        $PnS Name used for parameter n.
        $PnR Range for parameter number n.
        $PnB Number of bits reserved for parameter number n.
        $PnE Amplification type for parameter n.
        把每个通道按照NBRSE这几个存在的类别进一步分割
        """
        for i in range(1, channel_num+1):
            info["$P%dN" % i] = self.channel_name[i-1] if self.channel_name[i-1] is not None else ""
            info["$P%dS" % i] = self.marker_name[i-1] if self.marker_name[i-1] is not None else ""
            info["$P%dR" % i] = str(int(max(self.data[i-1])+1))
            info["$P%dB" % i] = "32"
            info["$P%dE" % i] = "0,0"
        return info

    def __write_header_txt(self, f):
        info_keys = list(self.info.keys())
        info_list = [""] * len(info_keys) * 2
        for i in range(0, len(info_keys)):
            key = info_keys[i]
            info_list[2 * i] = key
            info_list[2 * i + 1] = self.info[key]
        txt_str = "|" + "|".join(info_list) + "|"  # 前面加一个|, 后面加一个|

        # 二进制字符串与正常字符串长度不是完全一致
        txt_str = bytes(txt_str.encode("utf-8"))
        txt_str_bytes = len(txt_str)
        txt_start = "58"
        txt_end = str(txt_str_bytes + int(txt_start) - 1)

        # 在header部分只记录txt的位置信息
        # data和analysis的位置信息由txt中的$BEGINDATA, $ENDDATA, $BEGINANALYSIS, $ENDANALYSIS记录
        header_str = "FCS3.0" + " " * 4
        header_str = header_str + str(txt_start.center(8, " ")) + str(txt_end.center(8, " "))
        header_str = header_str + str("0".center(8, " ")) * 4
        header_str = bytes(header_str.encode("utf-8"))

        # 写入head部分, 再写入txt部分
        f.write(header_str)
        f.seek(int(txt_start))
        f.write(txt_str)

    def __write_data(self, f):
        """
        写入数据data
        """
        event_num = int(self.info["$TOT"])
        par_num = int(self.info["$PAR"])
        row_fmt = ">"+"f"*par_num

        f.seek(5000)
        t_start = datetime.datetime.now()
        # 开始写入data
        for index in range(0, event_num):
            tmp_row_data = tuple([self.data[col][index] for col in range(0, par_num)])
            tmp_unpack_data = struct.pack(row_fmt, *tmp_row_data)
            f.write(tmp_unpack_data)

        t_end = datetime.datetime.now()
        print("write %s elapse %s" % (self.info["$FIL"], (t_end - t_start)))

