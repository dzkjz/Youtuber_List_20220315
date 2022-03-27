from Data.Excel_Initializer import YoutuberExcelInitializer


class Youtuber:

    def __init__(self):
        self.__channel_url__ = ''
        self.__channel_subscribers_count__ = ''
        self.__channel_location__ = ''
        self.__channel_email__ = ''
        self.__channel_email_view_link__ = ''
        self.__channel_facebook__ = ''
        self.__channel_twitter__ = ''
        self.__channel_instagram__ = ''
        self.__channel_other_social__ = ''
        self.__channel_description__ = ''
        self.__channel_name__ = ''
        self.__source_keywords__ = ''

    def set_location(self, location):
        self.__channel_location__ = location

    def get_location(self):
        return self.__channel_location__

    def set_subscribers_count(self, subscribers_count):
        self.__channel_subscribers_count__ = subscribers_count

    def get_subscribers_count(self):
        return self.__channel_subscribers_count__

    def set_email(self, email):
        self.__channel_email__ = email

    def get_email(self):
        return self.__channel_email__

    def set_email_view_link(self, email_view_link):
        self.__channel_email_view_link__ = email_view_link

    def get_email_view_link(self):
        return self.__channel_email_view_link__

    def set_facebook(self, fb):
        self.__channel_facebook__ = fb

    def get_facebook(self):
        return self.__channel_facebook__

    def set_twitter(self, twitter):
        self.__channel_twitter__ = twitter

    def get_twitter(self):
        return self.__channel_twitter__

    def set_instagram(self, ig):
        self.__channel_instagram__ = ig

    def get_instagram(self):
        return self.__channel_instagram__

    def set_other_social(self, other_social_channel):
        self.__channel_other_social__ = other_social_channel

    def get_other_social(self):
        return self.__channel_other_social__

    def set_description(self, description):
        self.__channel_description__ = description

    def get_desciption(self):
        return self.__channel_description__

    def set_channel_name(self, name):
        self.__channel_name__ = name

    def get_channel_name(self):
        return self.__channel_name__

    def set_channel_source_keyword(self, source_keyword):
        self.__source_keywords__ = source_keyword

    def get_channel_source_keyword(self):
        return self.__source_keywords__

    def set_channel_url(self, url):
        self.__channel_url__ = url

    def get_channel_url(self):
        return self.__channel_url__

    def save_to_excel(self):
        # excel初始化
        excel = YoutuberExcelInitializer()
        # 新插入一行
        excel.NewRow(self)

    def duplicate_check(self):
        # excel初始化
        excel = YoutuberExcelInitializer()
        # 检测重复
        return excel.DuplicateCheck(self)
