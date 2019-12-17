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
import copy
import pandas as pd


class HeaderBef(object):
    def __init__(self, txt, filename):
        self.header_bef = ""
        self.position = {}

        self.__is_fcs_file(txt=txt, filename=filename)
        self.__get_header_bef(txt=txt)

    @staticmethod
    def __is_fcs_file(txt, filename):
        """
        判断是否是一个fcs3.0文件
        :return:
        """
        # fcs文件的格式，一般是3.0, 如果不是fcs3.0，抛出异常
        file_format = str(txt[0:6], encoding="utf-8")
        try:
            if file_format == "FCS3.0":
                # print("%s 是FCS3.0文件" % self.filename)
                return
            else:
                file_format_error = Exception(filename + "不是一个FCS3.0的文件")
                raise file_format_error
        except Exception as result:
            sys.stderr.write(str(result)+"\n")

    def __get_header_bef(self, txt):
        """
        获取fcs文件中，head起始和结束位置，data起始和结束位置，analysis起始和结束位置
        文件位置从0开始算的, 读取文件时，文件指针从1开始算
        :return:
        """
        self.header_bef = str(txt[0:58], encoding="utf-8")
        # head的起始位置和终止位置
        head_start = int(str(txt[10:18], encoding="utf-8").strip(" "))
        head_end = int(str(txt[18:26], encoding="utf-8").strip(" "))
        # 数据的起始位置和终止位置
        data_start = int(str(txt[26:34], encoding="utf-8").strip(" "))
        data_end = int(str(txt[34:42], encoding="utf-8").strip(" "))
        # 分析的起始位置和终止位置
        analysis_start = int(str(txt[42:50], encoding="utf-8").strip(" "))
        analysis_end = int(str(txt[50:58], encoding="utf-8").strip(" "))

        self.position["head_start"] = head_start
        self.position["head_end"] = head_end
        self.position["data_start"] = data_start
        self.position["data_end"] = data_end
        self.position["analysis_start"] = analysis_start
        self.position["analysis_end"] = analysis_end


class Header(object):
    def __init__(self, txt, file_name):
        self.header = ""
        self.info = {}
        self.__get_info(txt=txt, file_name=file_name)

    def __get_info(self, txt, file_name):
        """
        把 header_str分割，生成info字典
        """
        self.header = str(txt, encoding="utf-8")

        # 获取分隔符
        sep = self.header[0]
        fields = self.header.split(sep)
        fields.pop(0)  # 去除分割产生的第一个空字符串
        fields.pop(len(fields)-1)  # 去除分割产生的最后一个空字符串

        # 使用列表推导式分别获得key和对应的值
        key = [fields[i].upper() for i in range(0, len(fields)) if i % 2 == 0]
        val = [fields[i] for i in range(0, len(fields)) if i % 2 == 1]

        # 使用字典推导式获得info
        self.info = {key[i]: val[i] for i in range(0, len(key))}

        # 判断是否存在 $FIL这个信息
        if "$FIL" not in self.info:
            self.info["$FIL"] = file_name

        # xshif的fcs文件中的$FIL是一个带有绝对路径的文件名称,去掉名称中的路径
        self.info["$FIL"] = self.info["$FIL"].split("/")[-1]

        # 判断是否带有补偿矩阵
        if "$SPILLOVER" in self.info.keys():
            print("The File has compensation Matrix!")

        # 判断analysis部分是否不为空
        if self.info["$NEXTDATA"] != "0":
            sys.stderr.write("Some other data exist in the file but hasn't been parsed.\n")

        print("%s events were detected; Each event is characterized by %s parameters" % (self.info["$TOT"], self.info["$PAR"]))


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
    __count = 0  # 计数，总共有多少个fcs文件
    __fcs_file = []
    __fcs_object = []

    __channel_num = []
    __channel_name = []
    __stain_channel_num = []
    __stain_channel_name = []

    def __init__(self, file):
        """
        fcs文件属性，主要由header_bef, header, data三个部分构成
        """
        self.file_dir = "/".join(file.split('/')[0:-1])
        self.file_name = file.split('/')[-1]

        self.header_bef = None
        self.header = None
        self.pars = []
        self.stain_channels_index = []
        self.read(file)

        # 记录fcs对象信息
        Fcs.__add_class_attribute(self=self)

    def read(self, file):
        f = open(file, 'rb')
        txt = f.read()
        f.close()

        header_bef_txt = txt[0:58]
        self.header_bef = HeaderBef(header_bef_txt, self.file_name)

        header_txt = txt[self.header_bef.position["head_start"]:self.header_bef.position["head_end"]+1]
        self.header = Header(header_txt, self.file_name)

        self.__get_parameter()
        self.__get_stain_channels()

        t_start = datetime.datetime.now()
        data_txt = txt[self.header_bef.position["data_start"]:self.header_bef.position["data_end"]+1]
        self.__get_data(data_txt)
        t_end = datetime.datetime.now()
        print("read %s elapse %s" % (self.header.info["$FIL"], (t_end - t_start)))

    def __get_parameter(self):
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
        header = self.header
        # 字节顺序
        if header.info["$BYTEORD"] == "4,3,2,1":
            endianness = ">"
        else:
            endianness = "<"
            assert header.info["$BYTEORD"] == "1,2,3,4"

        if header.info["$DATATYPE"] != "F":
            raise NotImplementedError

        for i in range(1, int(header.info["$PAR"]) + 1):
            par_short_name = header.info["$P%dN" % i] if "$P"+str(i)+"N" in header.info else None
            par_name = header.info["$P%dS" % i] if "$P"+str(i)+"S" in header.info else None
            par_range = header.info["$P%dR" % i] if "$P"+str(i)+"R" in header.info else None
            par_bits = header.info["$P%dB" % i]
            par_amp = header.info["$P%dE" % i] if "$P"+str(i)+"E" in header.info else None

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
            data = [0]*int(header.info["$TOT"])
            par = Parameter(par_short_name, par_name, par_range, par_bits, par_amp, nb_bytes, fmt, data)
            self.pars.append(par)

    def __get_stain_channels(self):
        """
        找出染色的通道
        :return: 返回染色通道的索引
        """
        for i in range(0, len(self.pars)):
            channel_name = self.pars[i].par_name
            if channel_name is None:
                continue
            # 判断channel_name是否是 数字+字母+_marker的模式
            elif re.match("\d+.+_", channel_name):
                # 判断channel_name中是否包含DNA|cisplatin|barcode字符
                if re.search("DNA|cisplatin|barcode", channel_name):
                    continue
                else:
                    self.stain_channels_index.append(i+1)

    def __get_data(self, data_txt):
        """
        fcs_data得到的是字节Byte形式存储的,数据存储以字节为单位，数据传输通常以位bit为单位，通常一字节是8位bit
        len(fcs_data)给出有多少字节
        """
        # unpack data
        data_len = 0
        for row in range(0, int(self.header.info["$TOT"])):
            for column in range(0, int(self.header.info["$PAR"])):
                par = self.pars[column]
                nb_bytes = int(par.nb_bytes)
                # 二进制数据根据每个通道的存储字节来转换成常规数值
                value = struct.unpack(par.fmt, data_txt[data_len:data_len + nb_bytes])[0]
                data_len = data_len + nb_bytes
                self.pars[column].data[row] = value

    def __creat_dir(self, folder_name):
        # 在原有fcs路径下创建指定文件夹
        save_dir = self.file_dir + "/" + folder_name
        # excel文件夹不存在时创建
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        return save_dir

    def fcs2excel(self, folder_name="Excel"):
        """
        将fcs文件信息写出到excel中
        """
        pars = self.pars

        t_start = datetime.datetime.now()
        # 写入抬头信息
        marker_name = [re.sub("^.+?_", "", par.par_name) if par.par_name is not None else par.par_short_name for par in pars]
        marker_name = [marker_name[i] if marker_name[i] != "" else pars[i].par_short_name for i in range(0, len(pars))]

        data = [par.data for par in pars]
        df = pd.DataFrame(data).T
        df.columns = marker_name
        print(df.head())
        # 绝对路径
        save_dir = self.__creat_dir(folder_name)
        file = save_dir + "/" + self.file_name[0:-4] + ".csv"  # 去掉文件后缀.fcs
        df.to_csv(file, index=False)
        t_end = datetime.datetime.now()
        print("write %s to excel elapse %s" % (self.file_name, (t_end - t_start)))

    def delete_channel(self, *args, folder_name="Delete_Channel_Fcs"):
        """
        删除指定通道，传入进来的可以是通道数字，如89， 103， 104，或者是通道完整名字
        """
        pars = copy.deepcopy(self.pars)
        channel_name_1 = [par.par_short_name for par in pars]
        channel_name_2 = [re.sub("[^\d+]", "", name) for name in channel_name_1]
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

        # 写出到fcs
        save_dir = self.__creat_dir(folder_name)
        file = save_dir + "/" + self.file_name
        channel_name = [par.par_short_name for par in pars]
        marker_name = [par.par_name for par in pars]
        data = [par.data for par in pars]
        Write(file, channel_name, marker_name, data)

    def add_channel(self, *args, folder_name="Add_Channel_Fcs"):
        """
        往数据中添加一个通道及数据, 传进来的是(（channel_name, marker_name, data）, （channel_name, marker_name, data）)形式
        """
        pars = copy.deepcopy(self.pars)
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
            new_par = Parameter(par_short_name, par_name, par_range, par_bits, par_amp, nb_bytes, fmt, data)
            pars.append(new_par)

        # 写出到fcs
        save_dir = self.__creat_dir(folder_name)
        file = save_dir + "/" + self.file_name
        channel_name = [par.par_short_name for par in pars]
        marker_name = [par.par_name for par in pars]
        data = [par.data for par in pars]
        Write(file, channel_name, marker_name, data)

    def marker_rename(self, *args, folder_name="Marker_rename"):
        """
        修改marker_name,传入如(115，"CD3"), (89, "cd45), 或(通道完整名字，marker名字)
        """
        pars = copy.deepcopy(self.pars)
        channel_name_1 = [par.par_short_name for par in pars]
        channel_name_2 = [re.sub("[^\d+]", "", name) for name in channel_name_1]
        # 查找要修改marker名称的通道的索引
        for tmp_arg in args:
            tmp_rename_channel = str(tmp_arg[0])
            try:
                index = channel_name_1.index(tmp_rename_channel)
            except ValueError:
                index = channel_name_2.index(tmp_rename_channel)
            # 修改marker name
            marker_name = pars[index].par_name
            marker_name = '_'.join([marker_name.split("_")[0], tmp_arg[1]])
            pars[index].par_name = marker_name

        # 写出到fcs
        save_dir = self.__creat_dir(folder_name)
        file = save_dir + "/" + self.file_name
        channel_name = [par.par_short_name for par in pars]
        marker_name = [par.par_name for par in pars]
        data = [par.data for par in pars]
        Write(file, channel_name, marker_name, data)

    def down_sample(self):
        """
        对数据进行降采样
        """
        pass

    @classmethod
    def __add_class_attribute(cls, self):
        """
        添加类属性
        :param self: fcs对象
        """
        # 创建一个实例，计数加1
        cls.__count += 1
        cls.__fcs_file.append(self.file_name)
        cls.__fcs_object.append(self)

        cls.__channel_num.append(int(self.header.info["$PAR"]))  # 通道数量
        cls.__stain_channel_num.append(len(self.stain_channels_index))  # 染色通道数量

        # 记录通道名字和染色通道名字
        channel_name = [par.par_short_name for par in self.pars]
        cls.__channel_name.append(channel_name)
        cls.__stain_channel_name.append([channel_name[index-1] for index in self.stain_channels_index])

    @classmethod
    def __check_equally(cls, my_list):
        my_list = [element for element in my_list if element is not None]
        iterator = iter(my_list)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    @classmethod
    def check_channel_equally(cls, channel_num, channel_name, print_str="通道"):
        """
        检查fcs文件之间是否通道/染色通道一致
        """
        channel = {}
        for num in set(channel_num):
            num_index = [index for index in range(0, len(channel_num)) if channel_num[index] == num]
            channel[num] = num_index
        # 检查通道数量是否一致
        if len(channel) == 1:
            print("")
            for key in channel.keys():
                tmp_channel_name = [channel_name[index] for index in channel[key]]
                if cls.__check_equally(tmp_channel_name):
                    print("所有的fcs文件%s一致" % print_str)
                    return True
                else:
                    print("所有的fcs文件,%s数量一致但不相等" % print_str)
                    return False
        elif len(channel) != 1:
            print("")
            for key in channel.keys():
                tmp_channel_name = [channel_name[index] for index in channel[key]]
                current_file = "|".join([cls.__fcs_file[index].split("/")[-1][0:-4] for index in channel[key]])
                if cls.__check_equally(tmp_channel_name):
                    print("%s数量%d且一致的文件有:%s" % (print_str, key, current_file))
                else:
                    print("%s数量%d但不一致的文件有:%s" % (print_str, key, current_file))
            return False

    @classmethod
    def panel_rename(cls):
        """
        根据panel表，修改fcs文件marker name
        """
        # 先检查是不是所有的fcs文件染色通道一致
        if Fcs.check_channel_equally(Fcs.__stain_channel_num, Fcs.__stain_channel_name, print_str="染色通道"):
            print("")
            print("读取panel表,开始修改marker name")
            # 读取panel表信息
            panel_file = cls.__fcs_object[0].file_dir + "/panel.xlsx"
            workbook = xlrd.open_workbook(panel_file)
            panel_sheet = workbook.sheet_by_name('panel')

            channel = panel_sheet.col_values(0)
            channel = [re.sub("[^\d+]", "", tmp_channel) for tmp_channel in channel]

            marker = panel_sheet.col_values(1)
            marker = [re.sub("（", "(", tmp_marker) for tmp_marker in marker]
            marker = [re.sub("）", ")", tmp_marker) for tmp_marker in marker]

            global panel_tuple
            if len(channel) == len(marker):
                panel_tuple = tuple([(channel[i], marker[i]) for i in range(0, len(channel))])
            else:
                print("panel表中的channel和marker数量不一致！！！")

            for fcs in cls.__fcs_object:
                # 传入的是嵌套元组
                fcs.marker_rename(*panel_tuple)  # 传入panel表中的（通道名字，marker名字）

    @classmethod
    def merge(cls):
        """
        合并fcs文件
        """
        pass


class StainFcs(Fcs):
    def __init__(self, file):
        super().__init__(file)
        # 删除pars中对应的通道
        self.pars = [self.pars[i] for i in range(0, len(self.pars)) if i+1 in self.stain_channels_index]


class ClusterFcs(Fcs):
    pass
    """
    1. 改cluster-id
    2. 合并cluster-id
    """
    pass


class Write(object):
    def __init__(self, file, channel_name, marker_name, data):
        # 传入的filename是一个绝对路径
        self.file = file
        self.channel_name = channel_name
        self.marker_name = marker_name
        self.data = data
        self.__check_length()

        self.info = self.export_info()

        self.header_bef_str = ""
        self.header_str = ""
        self.__join_header_str()
        self.__join_header_bef_str()

        t_start = datetime.datetime.now()
        self.__write_fcs()
        t_end = datetime.datetime.now()
        print("write %s elapse %s" % (self.info["$FIL"], (t_end - t_start)))

    def __check_length(self):
        data_length_set = {len(tmp_data) for tmp_data in self.data}
        if len(data_length_set) != 1:
            print("传入的通道数据长度不一致！！！")
            assert len(data_length_set) == 1

        if len({len(self.channel_name), len(self.marker_name), len(self.data)}) != 1:
            print("传入的通道和marker, data数量不一致！！！")
            print("通道数量：%d, marker数量：%d, data数量：%d" % (len(self.channel_name), len(self.marker_name), len(self.data)))
            assert {len(self.channel_name), len(self.marker_name), len(self.data)} == 1

    def export_info(self):
        """
        组装出fcs文件的header信息
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
        info["$BEGINSTEXT"] = "0"
        info["$ENDSTEXT"] = "0"
        info["$NEXTDATA"] = "0"
        info["$BEGINANALYSIS"] = "0"
        info["$ENDANALYSIS"] = "0"
        info["ORIGINALGUID"] = "1.fcs"
        info["GUID"] = "1.fcs"

        channel_num = len(self.channel_name)
        info["$PAR"] = str(channel_num)
        event_num = len(self.data[0])
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
            info["$P%dR" % i] = str(max(self.data[i-1]))
            info["$P%dB" % i] = "32"
            info["$P%dE" % i] = "0,0"
        return info

    def __join_header_str(self):
        """
        根据组装出的info生成header
        """
        info_keys = list(self.info.keys())
        head_info = [""] * len(info_keys) * 2
        for i in range(0, len(info_keys)):
            key = info_keys[i]
            head_info[2 * i] = key
            head_info[2 * i + 1] = self.info[key]

        self.header_str = "|" + "|".join(head_info) + "|"  # 前面加一个|, 后面加一个|

    def __join_header_bef_str(self):
        """
        根据data字节数和header字节数算出每个部分的位置信息
        """
        # 所有字节数量
        data_bytes = int(self.info["$TOT"])*int(self.info["$PAR"])*4
        header_bytes = len(bytes(self.header_str.encode("utf-8")))  # 注意，有时候二进制字符串与正常字符串长度不一样

        # 文件位置从0开始算的
        # 前58个字节分别是
        # 是FCS3.0(6)+4个空格(4)+head_start(8)+head_end(8)+data_start(8)+data_end(8)+analysis_start(8)+analysis_end(8)
        # 文件内容从0开始算，文件指针从1开始算
        # 59至（header_bytes+59-1）个字节：header
        # head的开始位置记录规定小1，head_start = 59-1, head_end = header_bytes+head_start
        # （head_end+1+1）至（data_bytes+(head_end+1+1)-1）个字节: data
        # data_start = head_end+1, data_end = data_bytes+(head_end+1)
        # analysis_start = 0
        # analysis_end = 0

        position = {}

        head_start = 58
        head_end = header_bytes + head_start - 1
        data_start = head_end + 1
        data_end = data_bytes + data_start - 1
        analysis_start = 0
        analysis_end = 0

        position["head_start"] = head_start
        position["head_end"] = head_end
        position["data_start"] = data_start
        position["data_end"] = data_end
        position["analysis_start"] = analysis_start
        position["analysis_end"] = analysis_end
        position_keys = ["head_start", "head_end", "data_start", "data_end", "analysis_start", "analysis_end"]
        # 拼接header_bef_str
        self.header_bef_str = "FCS3.0" + " " * 4
        for key in position_keys:
            self.header_bef_str = self.header_bef_str + str(position[key]).center(8, " ")

    def __write_fcs(self):
        """
        将数据写入到fcs文件中
        先写入header之前的位置信息
        再写入header信息
        最后写入data
        """
        f = open(self.file, 'a+b')
        # 写入head前的信息, 再写入head
        txt = "".join([self.header_bef_str, self.header_str])
        txt = bytes(txt.encode("utf-8"))  # 先以utf-8标准编码，每个字符对应规则下的固定字节
        f.write(txt)
        # 开始写入data
        fmt = ">f"
        for index in range(0, int(self.info["$TOT"])):
            for tmp_data in self.data:
                tmp_unpack_data = struct.pack(fmt, tmp_data[index])
                f.write(tmp_unpack_data)
        f.close()

