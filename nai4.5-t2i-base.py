import requests
import json
import msgpack
import zipfile
import io
import os
import re
import random
from datetime import datetime

# 填入API KEY。以pst开头
API_KEY = ""


# 提示词 配置
PROMPT = "{{flat color}},{{rasusurasu,hagoonha,topia,nakkar}},[[kabocya_na,tantan_men_(dragon)]],year_2023,year_2023,    1girl, animal ears, pink hair, thighhighs, school uniform, solo, white thighhighs, pink eyes, animal ear fluff, long hair, skirt, sitting, wariza, serafuku, hair ornament, yellow cardigan, cardigan, ribbon, blush, shoes, ahoge, looking at viewer, zettai ryouiki, sailor collar, shirt, white background, flower, hairclip, cat ears, hand between legs, green skirt, between legs, brown footwear, open cardigan, hair ribbon, white shirt, open clothes, simple background, miniskirt"

NEGATIVE_PROMPT = "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], weibo watermark,{{{{{chibi,dragon girl}}}}}{{{+_+ }}}"


# 设置为 None 使用随机种子，或设置为具体数字使用固定种子
FIXED_SEED = None  

# API endpoint
url = "https://image.novelai.net/ai/generate-image"



# 请求体
payload = {
    "input": PROMPT,
    "model": "nai-diffusion-4-5-full",
    "action": "generate",
    "parameters": {
        "params_version": 3,
        "width": 832,
        "height": 1216,
        "scale": 6,
        "sampler": "k_dpmpp_2m",
        "steps": 28,
        "seed": FIXED_SEED if FIXED_SEED is not None else random.randint(10000000, 9999999999),
        "n_samples": 1,
        "ucPreset": 4,
        "qualityToggle": False,
        "dynamic_thresholding": False,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": True,
        "cfg_rescale": 0,
        "noise_schedule": "exponential",
        "legacy_v3_extend": False,
        "skip_cfg_above_sigma": 58,
        "v4_prompt": {
            "caption": {
                "base_caption": PROMPT,
                "char_captions": []
            },
            "use_coords": False,
            "use_order": True
        },
        "v4_negative_prompt": {
            "caption": {
                "base_caption": NEGATIVE_PROMPT,
                "char_captions": []
            },
            "legacy_uc": False
        },
        "negative_prompt": NEGATIVE_PROMPT,
        "stream": "msgpack"
    }
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def sanitize_filename(filename):
    """清理文件名，移除不合法的字符"""
    # 移除或替换文件名中的非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 限制文件名长度
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def generate_filename_from_prompt(prompt):
    """从prompt生成合适的文件名"""
    # 提取prompt中的关键词（去除特殊符号）
    # 移除大括号、方括号等特殊符号
    cleaned_prompt = re.sub(r'[{}\[\](),]', ' ', prompt)
    # 提取主要关键词
    keywords = cleaned_prompt.split()[:10]  # 取前10个关键词
    # 过滤掉太短的词
    keywords = [k for k in keywords if len(k) > 2]
    # 生成文件名
    filename_base = '_'.join(keywords[:5])  # 使用前5个关键词
    # 添加时间戳避免重复
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{filename_base}_{timestamp}"


try:
    seed_value = payload["parameters"]["seed"]
    print(f"正在生成，提示词为: {PROMPT}")
    print(f"使用的随机种子: {seed_value}")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("请求成功！")
        
        # 生成基础文件名
        base_filename = generate_filename_from_prompt(PROMPT)
        base_filename = sanitize_filename(base_filename)
        
        # 创建输出目录（如果不存在）
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # 检查响应是否为ZIP文件
        try:
            # 尝试将响应内容作为ZIP文件打开
            zip_buffer = io.BytesIO(response.content)
            with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                # 获取ZIP文件中的所有文件名
                file_list = zip_file.namelist()
                print(f"发现 {len(file_list)} 个图片文件")
                
                # 解压所有文件
                for idx, filename in enumerate(file_list):
                    # 读取文件内容
                    image_data = zip_file.read(filename)
                    
                    # 生成新的文件名
                    if len(file_list) > 1:
                        new_filename = f"{base_filename}_{idx}.png"
                    else:
                        new_filename = f"{base_filename}.png"
                    
                    # 保存文件
                    output_path = os.path.join(output_dir, new_filename)
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    print(f"图片已保存为: {output_path}")
                    
        except zipfile.BadZipFile:
            # 如果不是ZIP文件，可能是单个图片文件
            print("响应不是ZIP文件，尝试作为单个图片保存")
            output_path = os.path.join(output_dir, f"{base_filename}.png")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"图片已保存为: {output_path}")
            
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print(f"错误信息：{response.text}")
        
except Exception as e:
    print(f"错误：{e}")