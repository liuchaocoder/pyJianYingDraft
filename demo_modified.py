# 导入模块
import os
import datetime
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange, tim, Jianying_controller, Export_resolution, Export_framerate
import shutil
import urllib.request
import numpy as np
import time
try:
    from PIL import Image
    import imageio
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# 获取今天日期
today = datetime.datetime.now().strftime("%m月%d日")

# 保存路径
DRAFT_BASE_PATH = r"D:\jianji\anzhuang\JianyingPro Drafts"
DRAFT_FOLDER = os.path.join(DRAFT_BASE_PATH, today)

# 创建今天日期的文件夹（如果不存在）
os.makedirs(DRAFT_FOLDER, exist_ok=True)

DUMP_PATH = os.path.join(DRAFT_FOLDER, "draft_content.json")
print(f"草稿将保存到: {DUMP_PATH}")

# 创建素材文件夹
tutorial_asset_dir = os.path.join(os.path.dirname(__file__), 'readme_assets', 'tutorial')
if not os.path.exists(tutorial_asset_dir):
    os.makedirs(tutorial_asset_dir, exist_ok=True)
    print(f"创建素材文件夹: {tutorial_asset_dir}")

# 创建或下载示例素材
def create_sample_media():
    missing_files = []
    
    # 检查文件是否存在
    for file_path in [audio_path, video_path, gif_path]:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if not missing_files:
        print("所有素材文件已存在")
        return
    
    print(f"需要创建以下素材文件: {', '.join(os.path.basename(f) for f in missing_files)}")
    
    # 尝试下载示例文件
    try:
        # 音频示例
        if audio_path in missing_files:
            print(f"正在创建示例音频: {os.path.basename(audio_path)}")
            # 下载一个小的示例MP3文件
            audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            print(f"从 {audio_url} 下载音频文件...")
            urllib.request.urlretrieve(audio_url, audio_path)
            print(f"音频文件已保存到 {audio_path}")
        
        # 视频示例
        if video_path in missing_files:
            print(f"正在创建示例视频: {os.path.basename(video_path)}")
            # 使用示例视频 (这里可以使用示例视频URL或使用PIL创建一个简单的视频)
            video_url = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/big_buck_bunny_360p_1mb.mp4"
            print(f"从 {video_url} 下载视频文件...")
            urllib.request.urlretrieve(video_url, video_path)
            print(f"视频文件已保存到 {video_path}")
            
        # GIF示例
        if gif_path in missing_files and PIL_AVAILABLE:
            print(f"正在创建示例GIF: {os.path.basename(gif_path)}")
            # 创建一个简单的GIF
            frames = []
            for i in range(10):
                img = Image.new('RGB', (100, 100), color=(255, 0, 0))
                frames.append(np.array(img))
            
            imageio.mimsave(gif_path, frames, duration=0.1)
            print(f"GIF文件已保存到 {gif_path}")
            
    except Exception as e:
        print(f"创建素材文件时出错: {e}")
        print("请手动将音频、视频和GIF文件放置在 readme_assets/tutorial 文件夹中")
        exit(1)

# 创建剪映草稿
script = draft.Script_file(1920, 1080)  # 1920x1080分辨率

# 添加音频、视频和文本轨道
script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)

# 素材路径
audio_path = os.path.join(tutorial_asset_dir, 'audio.mp3')
video_path = os.path.join(tutorial_asset_dir, 'video.mp4')
gif_path = os.path.join(tutorial_asset_dir, 'sticker.gif')

# 创建示例素材
create_sample_media()

try:
    # 从本地读取音视频素材和一个gif表情包
    audio_material = draft.Audio_material(audio_path)
    video_material = draft.Video_material(video_path)
    gif_material = draft.Video_material(gif_path)
except Exception as e:
    print(f"读取素材文件时出错: {e}")
    print("请确保素材文件有效")
    exit(1)

# 创建音频片段
audio_segment = draft.Audio_segment(audio_material,
                                    trange("0s", "5s"),  # 片段将位于轨道上的0s-5s
                                    volume=0.6)          # 音量设置为60%(-4.4dB)
audio_segment.add_fade("1s", "0s")                       # 增加一个1s的淡入

# 创建视频片段
video_segment = draft.Video_segment(video_material, trange("0s", "4.2s"))  # 片段将位于轨道上的0s-4.2s
video_segment.add_animation(Intro_type.斜切)                               # 添加一个入场动画"斜切"

gif_segment = draft.Video_segment(gif_material,
                                  trange(video_segment.end, gif_material.duration))  # 紧跟上一片段，长度与gif一致

# 为二者添加一个转场
video_segment.add_transition(Transition_type.信号故障)  # 注意转场添加在"前一个"视频片段上

# 将上述片段添加到轨道中
script.add_segment(audio_segment).add_segment(video_segment).add_segment(gif_segment)

# 创建一个带气泡效果的文本片段并添加到轨道中
text_segment = draft.Text_segment(
    "测试pyJianYingDraft效果", video_segment.target_timerange,  # 文本片段的首尾与上方视频片段一致
    font=draft.Font_type.文轩体,                                # 设置字体为文轩体
    style=draft.Text_style(color=(1.0, 1.0, 0.0)),              # 字体颜色为黄色
    clip_settings=draft.Clip_settings(transform_y=-0.8)         # 位置在屏幕下方
)
text_segment.add_animation(draft.Text_outro.故障闪动, duration=tim("1s"))  # 添加出场动画"故障闪动", 设置时长为1s

# 尝试添加文本气泡效果（可能需要特定ID，如果失败可能需要跳过这步）
try:
    text_segment.add_bubble("361595", "6742029398926430728")  # 添加文本气泡效果
except Exception as e:
    print(f"添加文本气泡失败: {e}")

# 尝试添加花字效果（可能需要特定ID，如果失败可能需要跳过这步）
try:
    text_segment.add_effect("7296357486490144036")  # 添加花字效果
except Exception as e:
    print(f"添加花字效果失败: {e}")

script.add_segment(text_segment)

# 保存草稿（覆盖掉原有的draft_content.json）
print("正在保存草稿...")
script.dump(DUMP_PATH)

# 检查文件是否真正创建
if os.path.exists(DUMP_PATH) and os.path.getsize(DUMP_PATH) > 0:
    print(f"草稿已保存! 大小: {os.path.getsize(DUMP_PATH)} 字节")
else:
    print(f"警告: 草稿文件可能未正确保存，请检查权限或磁盘空间")
    exit(1)

print("==============================================================")
print("重要说明:")
print("1. 现在您需要先手动打开剪映，并在剪映中打开刚刚创建的草稿")
print(f"2. 草稿名称为: {today} (如 '04月30日')")
print("3. 手动打开草稿后，返回剪映主页，准备导出")
print("==============================================================")
print("请完成上述步骤后，再继续...")
input("按Enter键继续导出过程...")

try:
    # 初始化剪映控制器
    ctrl = Jianying_controller()
    
    # 确保剪映识别到了草稿
    print("正在检查剪映状态...")
    
    # 导出视频路径
    export_path = os.path.join(os.path.dirname(DRAFT_FOLDER), f"{today}_导出.mp4")
    
    # 导出草稿
    print(f"正在导出草稿到: {export_path}")
    
    try:
        ctrl.export_draft(today, export_path, 
                         resolution=Export_resolution.RES_1080P,
                         framerate=Export_framerate.FR_30)
        print("导出完成!")
    except draft.exceptions.DraftNotFound:
        print(f"错误: 未找到名为{today}的剪映草稿")
        print("解决方法: 请手动打开剪映，进入草稿，然后返回主页，让剪映识别草稿")
        print("如果草稿文件夹存在但剪映无法识别，请尝试重启剪映")
except Exception as e:
    print(f"导出过程中出错: {e}")
    print("请注意: 导出功能仅支持剪映6及以下版本且只在Windows系统上可用") 