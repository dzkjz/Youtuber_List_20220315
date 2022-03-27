import os.path
from Analyst.youtube_results_list_page import YoutubeResultsListPage
from Analyst.youtube_channel_page_analysis import YoutubeChannelPage

keywords_1 = ['सिक्के',
              'सपैसा बनाएं',
              'CoinDCX',
              'wazirx',
              'UnoCoin',
              'Zebpay',
              'BuyUCoin',
              'Kraken',
              'Kraken India',
              'Rupee', ]
keywords = [
    'CoinSwitch',
    'Bombay Stock Exchange',
    'National Stock Exchange',
    'Multi-Commodity Exchange',
    'National Commodity and Derivates Exchange',
    'India International Exchange',
    'NSE IFSC',
    'Indian Commodity Exchange',
    'Calcutta Stock Exchange',
    'Metropolitan Stock Exchange',
    'Ethereum',
    '₹',
    'CIBIL',
    'lakh',
    'ClearTax',
    'UPI',
    'PhonePe', 'binance',
    'huobi',
    'Airtel Money',
    'RTGS',
    'NEFT',
    'defi',
    'cryptocurrency',
    'nft',
    'DAO',
    'passive income',
    'cryptocurrencies',
    'bitcoin',
    'crypto',
    'make money',
    'Stock',
    'invest',
    'financial',
    'earn money',
]
headless = True
random_ua = False


def channel_page_preview():
    channel_file_path = "./Data/channels.txt"
    if os.path.exists(channel_file_path):
        file = open(channel_file_path)
        urls = file.read()
        urls = urls.splitlines()
        file.close()
        if len(urls) > 0:
            return True
    return False


def channel_page_solver(keyword, headless):
    youtube_channel = YoutubeChannelPage(keyword=keyword)
    channel_file_path = "./Data/channels.txt"
    if os.path.exists(channel_file_path):
        file = open(channel_file_path)
        urls = file.read()
        urls = urls.splitlines()
        file.close()
        if len(urls) > 0:
            url = urls[0]
            try:
                youtube_channel.Analysis(channel_url=url, headless=headless)
                # 移除已经成功取到值的
                with open(channel_file_path, "r") as f:
                    lines = f.readlines()
                    lines.remove(f"{url}\n")
                    if len(lines) == 0:
                        os.remove('./Data/keyword.txt')
                    with open(channel_file_path, "w") as new_f:
                        for line in lines:
                            new_f.write(line)
            except Exception:
                print(f"{url} 报错:{Exception.args}")


# youtube hashtag page
for keyword in keywords:
    # main process
    while channel_page_preview():
        # youtube channel page
        keyword_logged = open('./Data/keyword.txt', "r").readlines()[0]
        channel_page_solver(keyword_logged, headless=headless)

    youtube_results = YoutubeResultsListPage()
    youtube_results.Analysis(keywords=keyword, headless=headless, random_ua=random_ua)
