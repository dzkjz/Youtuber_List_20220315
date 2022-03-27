import pandas
import os
import pandas.errors
from pandas import DataFrame

'''requirements:
pip install pandas
pip install xlsxwriter
pip install xlrd
pip install openpyxl
'''


class YoutuberExcelInitializer:
    def __init__(self):
        self.__file_path__ = 'Data/youtuber-details.xlsx'
        self.__column_names__ = ['IndexCol', 'ChannelName', 'ChannelURL', 'SubscribersCount', 'Twitter', 'Facebook',
                                 'Instagram',
                                 'Email', 'Description', '点击链接登陆查看Email地址', 'Country', 'OtherSocialURL',
                                 'Category']
        self.__NewFile__()  # 新建表
        self.__InitializeColumn__()  # 初始化表

    def __NewFile__(self):
        """如果表不存在则新建"""
        if not os.path.exists(self.__file_path__):
            writer = pandas.ExcelWriter(self.__file_path__, engine='xlsxwriter')
            writer.save()

    def __InitializeColumn__(self):
        """初始化数据表"""
        # 读取数据表
        df_data = pandas.read_excel(self.__file_path__, sheet_name='Sheet1')
        # 循环查询数据表
        for column_name in self.__column_names__:
            # 检测当前列是否存在表中
            if column_name not in df_data.columns:
                # 新建一个列
                df_data[f'{column_name}'] = ''

        self.__SaveExcel__(data_frame=df_data)

    def __SaveExcel__(self, data_frame: DataFrame):
        data_frame.to_excel(self.__file_path__, sheet_name='Sheet1', index=False)

    def __read_index__(self):
        """获取当前数据表的最后序号"""
        df = pandas.read_excel(self.__file_path__, sheet_name='Sheet1', usecols=['IndexCol'])
        if df.empty:
            # print("空表")
            return 0
        else:
            tail = df.tail(1)  # 获取最后一行
            index = tail.iloc[0]['IndexCol']  # 获取最后一行的序号列的值
            # print(index)
            return index

    def DuplicateCheck(self, youtuber):
        df = pandas.read_excel(self.__file_path__, sheet_name='Sheet1',
                               usecols=['IndexCol', 'ChannelName', 'ChannelURL'])

        channel_url = youtuber.get_channel_url()
        # 判断ChannelURL所在行
        index = df.loc[df['ChannelURL'].str.contains(f'{channel_url}', case=False, regex=False)]['IndexCol'].index
        if len(index > 0):
            # 是否取到IndexCol值
            # 取index实际值
            index_val = index[0]
            if int(index_val) > 0:
                # 已经存在本行数据了
                print("重复数据")
                return True

        channel_name = youtuber.get_channel_name()
        # 判断ChannelName所在行
        index = df.loc[df['ChannelName'].str.contains(f'{channel_name}', case=False, regex=False, na=False)][
            'IndexCol'].index
        if len(index > 0):
            # 是否取到IndexCol值
            # 取index实际值
            index_val = index[0]
            if int(index_val) > 0:
                # 已经存在本行数据了
                print("重复数据")
                return True
        return False

    def NewRow(self, youtuber):

        if_is_duplicated = self.DuplicateCheck(youtuber)

        if if_is_duplicated:
            return
        df_origin = pandas.read_excel(self.__file_path__, sheet_name='Sheet1')

        # 获取历史最后行数
        index = self.__read_index__()
        # 当前行数+1
        index += 1
        # 获取数据
        channel_name = youtuber.get_channel_name().strip()
        channel_url = youtuber.get_channel_url().strip()
        channel_subscribers_count = str(youtuber.get_subscribers_count())
        channel_twitter = youtuber.get_twitter()
        channel_facebook = youtuber.get_facebook()
        channel_instagram = youtuber.get_instagram()
        channel_email = youtuber.get_email()
        channel_description = youtuber.get_desciption().strip()
        channel_email_link = youtuber.get_email_view_link()
        channel_country = youtuber.get_location().strip()
        channel_other_social = youtuber.get_other_social()
        channel_category = youtuber.get_channel_source_keyword().strip()

        # 格式构造
        data = {
            'IndexCol': [f"{index}"],
            'ChannelName': [channel_name],
            'ChannelURL': [channel_url],
            'SubscribersCount': [channel_subscribers_count],
            'Twitter': [channel_twitter],
            'Facebook': [channel_facebook],
            'Instagram': [channel_instagram],
            'Email': [channel_email],
            'Description': [channel_description],
            '点击链接登陆查看Email地址': [channel_email_link],
            'Country': [channel_country],
            'OtherSocialURL': [channel_other_social],
            'Category': [channel_category],
        }
        print(f'数据插入完成{data}')
        # 生成数据表框架
        new_df = pandas.DataFrame(data)
        df_new = pandas.concat([df_origin, new_df], axis=0)  # 追加到原始数据后面 [表合并]
        # 保存表
        self.__SaveExcel__(data_frame=df_new)
        # 提示
        print(f'{data}/t 数据插入完成!')
