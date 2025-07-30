# nai-v4.5-api
NovelAI diffusion V4.5 full模型RESTful api调用
## 使用前首先要获取NovelAI API key：
### 1.首先进入[Novelai官网](https://novelai.net/stories)，点击左上角中间那个齿轮标志
![image](https://github.com/user-attachments/assets/7593250e-977b-4c29-b9f2-5c2a2211edd0)
### 2.左侧栏找到Account，点击Get Persistent API Token：
![image](https://github.com/user-attachments/assets/616d75e0-e769-4214-ab09-7e723997257c)
### 3.将获得的API key复制下来
![image](https://github.com/user-attachments/assets/84e4670c-f682-48fe-a190-7124da80de71)
## 使用方法：
### 基本文生图：
将**nai4.5-t2i-base.py**脚本下载在本地，并将获得的API Key填在脚本的```API_KEY```变量中

直接使用python执行脚本：
```bash
python nai4.5-t2i-base.py
```

生成的图片将保存在脚本目录的generated_images文件夹中

### 基本图生图：
将**nai4.5-i2i.py**脚本下载在本地，API Key填在脚本的```API_KEY```变量中

修改脚本中的图生图专用参数：
   ```python
   # 1. 设置源图片路径
   SOURCE_IMAGE_PATH = "source_image.png"  # 修改为您的图片路径
   
   # 2. 调整强度参数（可选）
   STRENGTH = 0.1  # 0.1 表示轻微修改，0.9 表示大幅修改
   NOISE = 0.01    # 噪声量
   ```

然后直接使用python执行脚本：
```bash
python nai4.5-i2i.py
```
