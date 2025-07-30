# NAI V4.5图生图
# by 2575044704
import requests
import json
import base64
import zipfile
import io
import os
import re
import random
from datetime import datetime


API_KEY = ""

# Prompt 配置
PROMPT = "{{flat color}},{{rasusurasu,hagoonha,topia,nakkar}},[[kabocya_na,tantan_men_(dragon)]],year_2023,year_2023,    1girl, animal ears, pink hair, thighhighs, school uniform, solo, white thighhighs, pink eyes, animal ear fluff, long hair, skirt, sitting, wariza, serafuku, hair ornament, yellow cardigan, cardigan, ribbon, blush, shoes, ahoge, looking at viewer, zettai ryouiki, sailor collar, shirt, white background, flower, hairclip, cat ears, hand between legs, green skirt, between legs, brown footwear, open cardigan, hair ribbon, white shirt, open clothes, simple background, miniskirt"

NEGATIVE_PROMPT = "lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], weibo watermark,{{{{{chibi,dragon girl}}}}}{{{+_+ }}}"

# 源图片路径配置
SOURCE_IMAGE_PATH = r"/home/admin/nai-api/generated_images/flat_color_rasusurasu_hagoonha_topia_20250730_065129.png"  # 修改为您的源图片路径

# Seed 配置
# 设置为 None 使用随机种子，或设置为具体数字使用固定种子
FIXED_SEED = None  # 例如: FIXED_SEED = 12345678 使用固定种子

# 图生图参数配置
STRENGTH = 0.6  # 图像变化强度 (0-1)，值越大变化越大
NOISE = 0.4    # 噪声强度 (0-1)

# API endpoint
url = "https://image.novelai.net/ai/generate-image"



def image_to_base64(image_path):
    """将图片文件转换为 base64 编码"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"错误：找不到图片文件 '{image_path}'")
        return None
    except Exception as e:
        print(f"读取图片时出错：{e}")
        return None

def sanitize_filename(filename):
    """清理文件名，移除不合法的字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def generate_filename_from_prompt(prompt):
    """从prompt生成合适的文件名"""
    cleaned_prompt = re.sub(r'[{}\[\](),]', ' ', prompt)
    keywords = cleaned_prompt.split()[:10]
    keywords = [k for k in keywords if len(k) > 2]
    filename_base = '_'.join(keywords[:5])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"img2img_{filename_base}_{timestamp}"

# 读取并编码源图片
img_base64 = image_to_base64(SOURCE_IMAGE_PATH)
if not img_base64:
    print("无法继续，请确保源图片存在并且路径正确。")
    exit(1)

# 生成种子值
seed_value = FIXED_SEED if FIXED_SEED is not None else random.randint(10000000, 9999999999)
extra_noise_seed = seed_value - 1  # extra_noise_seed 通常比主种子小1

# 请求体
payload = {
    "input": PROMPT,
    "model": "nai-diffusion-4-5-full",
    "action": "img2img",
    "parameters": {
        "params_version": 3,
        "width": 832,
        "height": 1216,
        "scale": 6,
        "sampler": "k_dpmpp_2m",
        "steps": 28,
        "seed": seed_value,
        "n_samples": 1,
        "strength": STRENGTH,
        "noise": NOISE,
        "ucPreset": 4,
        "qualityToggle": False,
        "autoSmea": False,
        "dynamic_thresholding": False,
        "controlnet_strength": 1,
        "legacy": False,
        "add_original_image": True,
        "cfg_rescale": 0,
        "noise_schedule": "exponential",
        "legacy_v3_extend": False,
        "skip_cfg_above_sigma": 58,
        "use_coords": False,
        "normalize_reference_strength_multiple": True,
        "inpaintImg2ImgStrength": 1,
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
        "legacy_uc": False,
        "image": img_base64,
        "characterPrompts": [],
        "extra_noise_seed": extra_noise_seed,
        "color_correct": False,
        "negative_prompt": NEGATIVE_PROMPT,
        "stream": "msgpack"
    }
}
# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

try:
    print(f"正在进行图生图...")
    print(f"源图片: {SOURCE_IMAGE_PATH}")
    print(f"提示词: {PROMPT}")
    print(f"使用的随机种子: {seed_value}")
    print(f"强度: {STRENGTH}, 噪声: {NOISE}")
    
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