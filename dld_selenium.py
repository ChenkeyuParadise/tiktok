#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/env python
# coding=utf-8
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import time

from TikTok import TikTok

def get_dir_size(dir):
   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size


def progressBarDownload(url, filepath):
    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True, headers=headers)
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('[开始下载]:文件大小:{size:.2f} MB'.format(
                size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + '[下载进度]:%s%.2f%%' % (
                        '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
        end = time.time()  # 下载结束时间
        print('\n' + '[下载完成]:耗时: %.2f秒\n' % (
                end - start))  # 输出下载用时时间
    except Exception as e:
        # 下载异常 删除原来下载的文件, 可能未下成功
        if os.path.exists(filepath):
            os.remove(filepath)
        print("[  错误  ]:下载出错\r")
# 设置Chrome驱动的路径
chrome_driver_path = "/usr/local/bin/chromedriver"
os.environ["PATH"] += os.pathsep + '"/usr/local/bin/'
output_path_prefix = '/Users/bytedance/data/tt_download/tiktok/{query}/{video_id}'
# 初始化Chrome浏览器
#options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # 设置为无界面模式

# 搜索关键词
query_list = ["家长辅导",'情侣搞笑','整蛊搞笑','整蛊搞笑国外','熊孩子作死解气集合']
query_list = query_list[2:]
# query_list = ["家长"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
# 启动Chrome浏览器
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
tk = TikTok(3)
def get_video(tk, url, output_path):
    key_type, key = tk.getKey(url)
    datanew, dataraw = tk.getAwemeInfo(key)
    tk.awemeDownload(awemeDict=datanew, music=True, cover=True, avatar=True, savePath=output_path)

# 打开抖音搜索页面
for e_query in query_list:
    url = 'https://www.douyin.com/search/' + e_query
    browser.get(url)
    # 模拟人工搜索
    time.sleep(5)

    # 模拟滚动加载
    for i in range(3):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)

    # 获取视频链接和标题
    video_links = []
    video_titles = []
    #videos = browser.find_elements_by_css_selector('div.search-video-item')
    video_elements = browser.find_elements(By.CSS_SELECTOR, 'a[href*="douyin.com/video"]')
    for video_element in video_elements[:10]:
        video_link = video_element.get_attribute('href')
        print("video_link:", video_link)
        if video_link.find('?') != -1:
           url = video_link.split('?')[0]
        else:
           url = video_link
        key_type, key = tk.getKey(url)
        output_path = output_path_prefix.format(query=e_query, video_id=key)
        if os.path.exists(output_path):
            continue
        os.makedirs(output_path)
        try:
            get_video(tk, url, output_path)
        except Exception as e:
            print("[Exception]:", e)
            status = os.system('lux -o {out_dir} {video_url}'.format(video_url=url, out_dir=output_path))
        if os.path.exists(output_path):
            if get_dir_size(output_path) == 0:
                os.rmdir(output_path)
        #status = os.system('lux {video_url}'.format(video_url=url))
        print("dowload {video_url}; output dir: {output_path}".format(video_url=url, output_path=output_path))

# 关闭浏览器
#browser.quit()
