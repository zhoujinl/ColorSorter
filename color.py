import json
import math
import cv2
import numpy as np
from sklearn.cluster import KMeans
import argparse
import webcolors
from collections import Counter
import os

# 获取当前脚本文件所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, "colors.json")

with open(config_file) as clr:
    color_dict = json.load(clr)

def get_top_colors(image_path, num_colors=5):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 将图像转换为RGB格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Reshape图像为一维数组
    pixels = image.reshape((-1, 3))
    
    # 使用K-Means算法进行聚类，指定n_init参数
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(pixels)
    
    # 获取聚类中心作为主要颜色
    colors = kmeans.cluster_centers_
    
    # 将颜色值限制在0到255之间
    colors = colors.astype(int)
    
    # 计算每个聚类的像素数量
    pixel_counts = Counter(kmeans.labels_)
    
    # 计算每种颜色的占比
    total_pixels = len(pixels)
    color_ratios = [count / total_pixels for count in pixel_counts.values()]
    
    # 获取前num_colors个颜色及其占比
    top_colors = list(zip(colors, color_ratios))
    
    # 映射RGB值到颜色名称和Hex值
    top_colors_with_names = [
        (color, ratio, rgb_to_color_name(color), rgb_to_hex(color))
        for color, ratio in top_colors
    ]
    
     # 根据占比倒排序
    top_colors_with_names = sorted(top_colors_with_names, key=lambda x: x[1], reverse=True)

    
    return top_colors_with_names

def rgb_to_color_name(rgb_tuple):
    try:
        color_name = webcolors.rgb_to_name(rgb_tuple)
        return color_name
    except ValueError:
        # 如果找不到精确的匹配，可以选择最接近的颜色
        closest_name = find_closest_color(rgb_tuple)
        return closest_name if closest_name else "Unknown"

def find_closest_color(requested_colour):
    min_colors = {}
    for key, name in color_dict['color_names'].items():
        r_c, g_c, b_c = webcolors.hex_to_rgb("#"+key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colors[math.sqrt(rd + gd + bd)] = name
        #print(min(min_colours.keys()))
    return min_colors[min(min_colors.keys())]


def rgb_to_hex(rgb_tuple):
    # 将RGB元组转换为带有#前缀的十六进制颜色代码
    hex_value = "#{:02x}{:02x}{:02x}".format(*rgb_tuple)
    return hex_value


    
def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description='Get top colors from an image.')
    
    # 添加图像路径参数
    parser.add_argument('--image-path', type=str, help='Path to the input image')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用函数获取颜色信息
    top_colors = get_top_colors(args.image_path)
    
    # 打印结果
    result = []
    for color, ratio, color_name, hex_value in top_colors:
        result.append({'color': color, 'hex' : hex_value ,'ratio': ratio, 'name': color_name})
        print(f'Color: {color}, Hex: {hex_value}, Ratio: {ratio:.2%}, Name: {color_name}')
        

if __name__ == '__main__':
    main()
