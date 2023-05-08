#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/01/27 19:36:18
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''

import argparse
import os
import json
from TikTok import TikTok
from TikTokUtils import Utils


def argument():
    parser = argparse.ArgumentParser(description='抖音批量下载工具 使用帮助')
    parser.add_argument("--link", "-l",
                        help="1.作品(视频或图集)、合集、个人主页抖音分享链接(删除文案, 保证只有URL, https://v.douyin.com/kcvMpuN/)\r\n"
                             "2.解析直播网页版网址(https://live.douyin.com/802939216127)",
                        type=str, required=True)
    parser.add_argument("--path", "-p", help="下载保存位置",
                        type=str, required=True)
    parser.add_argument("--music", "-m", help="是否下载视频中的音乐(True/False), 默认为True",
                        type=bool, required=False, default=True)
    parser.add_argument("--cover", "-c", help="是否下载视频的封面(True/False), 默认为True, 当下载视频时有效",
                        type=bool, required=False, default=True)
    parser.add_argument("--avatar", "-a", help="是否下载作者的头像(True/False), 默认为True",
                        type=bool, required=False, default=True)
    parser.add_argument("--mode", "-M", help="link是个人主页时, 设置下载发布的作品(post)或喜欢的作品(like)或者用户所有合集(mix), 默认为post",
                        type=str, required=False, default="post")
    parser.add_argument("--deep", "-d", help="下载深度限制",
                        type=int, required=False, default=2)
    args = parser.parse_args()

    return args


def main():
    utils = Utils()
    args = argument()
    tk = TikTok(args.deep)
    url = tk.getShareLink(args.link)
    key_type, key = tk.getKey(url)
    print("key_type:", key_type)
    print("key:", key)
    if key is None or key_type is None:
        return
    elif key_type == "user" and args.mode != 'mix':
        datalist = tk.getUserInfo(key, args.mode, 35)
        tk.userDownload(awemeList=datalist, music=args.music, cover=args.cover, avatar=args.avatar,
                        savePath=args.path)
    elif key_type == "user" and args.mode == 'mix':
        if not os.path.exists(args.path):
            os.mkdir(args.path)
        mixIdNameDict = tk.getUserAllMixInfo(key, 35)

        for mix_id in mixIdNameDict:
            print(f'[  提示  ]:正在下载合集 [{mixIdNameDict[mix_id]}] 中的作品\r\n')
            mix_file_name = utils.replaceStr(mixIdNameDict[mix_id])
            datalist = tk.getMixInfo(mix_id, 35)
            tk.userDownload(awemeList=datalist, music=args.music, cover=args.cover, avatar=args.avatar,
                        savePath=os.path.join(args.path, mix_file_name))
            print(f'[  提示  ]:合集 [{mixIdNameDict[mix_id]}] 中的作品下载完成\r\n')
    elif key_type == "mix":
        datalist = tk.getMixInfo(key,35)
        tk.userDownload(awemeList=datalist, music=args.music, cover=args.cover, avatar=args.avatar,
                        savePath=args.path)
    elif key_type == "aweme":
        datanew, dataraw = tk.getAwemeInfo(key)
        tk.awemeDownload(awemeDict=datanew, music=args.music, cover=args.cover, avatar=args.avatar,
                         savePath=args.path)
    elif key_type == "live":
        live_json = tk.getLiveInfo(key)
        if not os.path.exists(args.path):
            os.mkdir(args.path)

        # 保存获取到json
        print("[  提示  ]:正在保存获取到的信息到result.json\r\n")
        with open(os.path.join(args.path, "result.json"), "w", encoding='utf-8') as f:
            f.write(json.dumps(live_json, ensure_ascii=False, indent=2))
            f.close()


if __name__ == "__main__":
    main()
