# pyJianYingDraft使用经验总结

## 项目概述

pyJianYingDraft是一个轻量级、灵活、易上手的Python剪映草稿生成及导出工具，可用于构建全自动视频剪辑/混剪流水线。

主要功能：
- 生成剪映草稿文件（创建轨道、添加素材、设置特效等）
- 模板模式（基于现有草稿进行修改）
- 批量导出草稿为视频

## 安装配置

安装方法：
```bash
pip install pyJianYingDraft
```

依赖库：
- pymediainfo
- imageio
- uiautomation (Windows系统下控制剪映UI)

推荐使用Python 3.8或3.11版本，部分用户反映Python 3.13可能存在兼容性问题。

## 正确使用流程

经过实践，我们发现使用pyJianYingDraft的正确流程如下：

### 创建草稿文件

1. **先在剪映中手动创建空白草稿**（这一步非常重要）
   - 打开剪映软件
   - 创建一个空白草稿（例如命名为"04月30日"）
   - 记住草稿文件夹路径

2. **退出剪映或返回剪映首页**

3. **使用pyJianYingDraft生成草稿内容**
   ```python
   import pyJianYingDraft as draft
   
   # 设置草稿文件路径
   DUMP_PATH = r"D:\jianji\anzhuang\JianyingPro Drafts\04月30日\draft_content.json"
   
   # 创建剪映草稿对象
   script = draft.Script_file(1920, 1080)
   
   # 添加轨道、素材、特效等
   script.add_track(draft.Track_type.audio)
   # ...添加其他内容...
   
   # 保存草稿
   script.dump(DUMP_PATH)
   ```

4. **验证草稿文件是否正确创建**
   ```python
   if os.path.exists(DUMP_PATH) and os.path.getsize(DUMP_PATH) > 0:
       print(f"草稿已保存! 大小: {os.path.getsize(DUMP_PATH)} 字节")
   else:
       print(f"警告: 草稿文件可能未正确保存")
   ```

### 导出草稿为视频

1. **打开剪映，并在剪映中手动打开生成的草稿**
   - 这一步很关键，确保剪映能识别到草稿

2. **返回剪映首页**

3. **使用pyJianYingDraft控制导出**
   ```python
   # 初始化剪映控制器
   ctrl = draft.Jianying_controller()
   
   # 导出草稿
   ctrl.export_draft("04月30日", "D:/输出视频.mp4", 
                    resolution=draft.Export_resolution.RES_1080P,
                    framerate=draft.Export_framerate.FR_30)
   ```

## 遇到的问题与解决方案

### 问题1：草稿文件夹存在但剪映不识别

**问题描述**：使用pyJianYingDraft创建了草稿文件（draft_content.json），在文件系统中可以看到，但剪映软件无法识别该草稿。

**解决方案**：
1. 必须先在剪映中手动创建空白草稿，然后用脚本生成的内容覆盖，而不是直接创建新文件夹
2. 覆盖后需要重启剪映或重新打开剪映，让它重新扫描草稿文件夹
3. 打开草稿后，保存一次草稿，确保剪映完全识别草稿内容

### 问题2：导出时提示"未找到名为XX的剪映草稿"

**问题描述**：使用`export_draft`导出时，显示"未找到名为XX的剪映草稿"错误。

**解决方案**：
1. 确保在导出前已在剪映中手动打开过该草稿
2. 导出前返回剪映首页，让剪映正确识别草稿
3. 检查草稿名称是否与代码中指定的完全一致（包括日期格式）

### 问题3：兼容性问题

**限制说明**：
- 模板模式仅支持剪映5.9及以下版本（因为6+版本对draft_content.json文件进行了加密）
- 批量导出功能仅支持剪映6及以下版本（因为7+版本隐藏了控件）
- 导出功能仅在Windows系统下可用（依赖uiautomation库）

## 关键经验总结

1. **遵循正确步骤**：必须先手动创建草稿，再用脚本修改内容，不能直接创建草稿文件
2. **手动激活草稿**：导出前必须手动在剪映中打开草稿，然后返回首页
3. **关注文件检查**：生成草稿后，验证文件是否成功创建并有内容
4. **版本兼容性**：注意剪映版本限制，不同版本支持的功能不同

## 未来定制开发方向

1. **改进草稿识别**：研究如何让剪映更可靠地识别生成的草稿
2. **支持更多版本**：探索剪映6+版本草稿文件的解密方式
3. **优化导出流程**：减少手动操作步骤，提高自动化程度
4. **扩展特效库**：增加对更多剪映特效的支持
5. **多素材管理**：改进批量素材的管理和引用方式

## 参考资料

- [pyJianYingDraft GitHub仓库](https://github.com/GuanYixuan/pyJianYingDraft)
- [剪映官方文档](https://www.capcut.cn/) 