# nai-v4.5-api
NovelAI diffusion V4.5 full模型RESTful api调用

## 使用前首先要获取NovelAI API key：
### 1.首先进入[Novelai官网](https://novelai.net/stories)，点击左上角中间那个齿轮标志
![image](https://github.com/user-attachments/assets/7593250e-977b-4c29-b9f2-5c2a2211edd0)
### 2.左侧栏找到Account，点击Get Persistent API Token：
![image](https://github.com/user-attachments/assets/616d75e0-e769-4214-ab09-7e723997257c)
### 3.将获得的API key复制下来
![image](https://github.com/user-attachments/assets/84e4670c-f682-48fe-a190-7124da80de71)

# 使用方法：

### 基本文生图：
1. 将**nai4.5-t2i-base.py**脚本下载在本地
2. 编辑脚本，在`API_KEY = ""`中填入您的API Key
3. 根据需要修改参数配置区域中的各项参数
4. 执行脚本：

```bash
python nai4.5-t2i-base.py
```
生成的图片将保存在脚本目录的generated_images文件夹中

### 基本图生图：
1. 将**nai4.5-i2i.py**脚本下载在本地
2. 编辑脚本，在`API_KEY = ""`中填入您的API Key
3. 修改脚本中的图生图专用参数：

```python
# 源图片路径配置
SOURCE_IMAGE_PATH = "source_image.png"  # 修改为您的图片路径

# ==================== 图生图专用参数 ====================
# 图生图参数配置
STRENGTH = 0.6  # 图像变化强度 (0-1)，值越大变化越大
NOISE = 0.4     # 噪声强度 (0-1)
```

4. 根据需要修改其他参数
5. 执行脚本：

```bash
python nai4.5-i2i.py
```

## 参数配置说明

### 基础参数配置
在脚本中找到对应的配置区域进行修改：

```python
# ==================== 基础配置 ====================
# 填入API KEY。以pst开头
API_KEY = ""

# 提示词配置
PROMPT = "your prompt here"  # 正向提示词
NEGATIVE_PROMPT = "your negative prompt"  # 负向提示词

# ==================== 图像参数配置 ====================
# 图像尺寸（必须是64的倍数）
WIDTH = 832    # 图像宽度
HEIGHT = 1216  # 图像高度

# 采样参数
SAMPLER = "k_dpmpp_2m"  # 采样器
STEPS = 28              # 迭代步数
SCALE = 6               # CFG Scale (引导强度)

# 种子设置
FIXED_SEED = None  # None为随机种子，或设置具体数字如：12345678

# 生成数量
N_SAMPLES = 1  # 单次生成图片数量

# ==================== 高级参数配置 ====================
# 负面提示词预设
UC_PRESET = 4  # 0-4，数字越高过滤越严格

# 高级调优参数
QUALITY_TOGGLE = False           # 质量开关
DYNAMIC_THRESHOLDING = False     # 动态阈值
CFG_RESCALE = 0                  # CFG重缩放（0-1）
NOISE_SCHEDULE = "exponential"   # 噪声计划
SKIP_CFG_ABOVE_SIGMA = 58        # 在高sigma值时跳过CFG
```

### 采样器选项
可用的采样器包括：
- `"k_euler"` - Euler
- `"k_euler_a"` - Euler_ancestor
- `"k_dpmpp_2s_a"` - DPM++ 2S ancestor
- `"k_dpmpp_2m"` - DPM++ 2M
- `"k_dpmpp_2m_sde"` - DPM++ 2M SDE
- `"k_dpmpp_sde"` - DPM++ SDE


### 分辨率预设
常用分辨率（宽x高）：
- `832 x 1216` - 竖版默认
- `1216 x 832` - 横版默认
- `1024 x 1024` - 正方形
- `1344 x 768` - 宽屏横版
- `768 x 1344` - 竖版手机壁纸
- `1920 x 1088` - 接近16:9
- `1088 x 1920` - 竖版高清

**注意**：分辨率大于832 x 1216会产生积分扣费
