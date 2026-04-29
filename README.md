# 抄袭调色盘（Plagiarism Palette）

一个可打包成 `.exe` 的桌面小工具：
- 左右两侧分别输入两段文本。
- 点击“检测重复”后，疑似重复内容会在两边同时高亮显示。
- 匹配不是纯机械逐字比对，支持一定“跳段”场景（基于序列匹配）。
- 顶部提供“文件名”输入框，方便标识当前任务文本。

## 运行方式（Python）

```bash
python plagiarism_palette.py
```

## 打包为 .exe（Windows）

1. 安装 PyInstaller：

```bash
pip install pyinstaller
```

2. 在项目目录执行：

```bash
pyinstaller --noconfirm --onefile --windowed --name 抄袭调色盘 plagiarism_palette.py
```

3. 生成文件位置：

- `dist/抄袭调色盘.exe`

## 使用说明

1. 在顶部输入文件名（例如：`作业A-对比.txt`）。
2. 左侧粘贴文本 A，右侧粘贴文本 B。
3. 点击“检测重复”。
4. 黄色高亮即为疑似重复片段。

## 作者

GPT-5.3-Codex
