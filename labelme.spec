# -*- mode: python -*-
# vim: ft=python

import sys
import os
from pathlib import Path

# 解决Windows递归限制问题
sys.setrecursionlimit(5000)

# 明确设置Labelme主程序路径（根据你的实际路径）
LABELME_MAIN = Path("labelme") / "__main__.py"

# 验证主程序文件是否存在
if not LABELME_MAIN.exists():
    raise FileNotFoundError(f"未找到主程序文件: {LABELME_MAIN}\n请确认路径是否为labelme/__main__.py")

# 确定labelme根目录（主程序所在目录）
LABELME_ROOT = LABELME_MAIN.parent  # 这会指向labelme目录

# 自动获取osam安装路径
try:
    import osam
    OSAM_PATH = Path(os.path.dirname(osam.__file__))
except ImportError:
    raise ImportError("请确保osam库已正确安装: pip install osam")

# 验证必要文件是否存在
required_files = [
    LABELME_MAIN,  # 主程序文件: labelme/__main__.py
    LABELME_ROOT / "config" / "default_config.yaml",  # 配置文件: labelme/config/default_config.yaml
    LABELME_ROOT / "icons" / "icon.ico",  # 图标文件: labelme/icons/icon.ico
    OSAM_PATH / "_models" / "yoloworld" / "clip" / "bpe_simple_vocab_16e6.txt.gz"  # OSAM词汇文件
]

# 检查文件并提供更详细的错误信息
for file in required_files:
    if not file.exists():
        if "config" in str(file):
            hint = f"请确认配置文件存在于: {LABELME_ROOT / 'config' / 'default_config.yaml'}"
        elif "icons" in str(file):
            hint = f"请确认图标文件存在于: {LABELME_ROOT / 'icons' / 'icon.ico'}"
        elif "bpe_simple_vocab" in str(file):
            hint = "请确认osam库已正确安装，且包含该词汇文件"
        else:
            hint = "请检查文件是否存在于该路径下"
        raise FileNotFoundError(f"必要文件不存在: {file}\n提示: {hint}")

a = Analysis(
    [str(LABELME_MAIN)],  # 使用正确的主程序路径: labelme/__main__.py
    pathex=[str(LABELME_ROOT.parent)],  # 设置项目根目录
    binaries=[],
    datas=[
        # Labelme配置文件 (源: labelme/config/default_config.yaml -> 目标: labelme/config)
        (str(LABELME_ROOT / "config" / "default_config.yaml"), "labelme/config"),
        # 图标文件 (源: labelme/icons/* -> 目标: labelme/icons)
        (str(LABELME_ROOT / "icons" / "*"), "labelme/icons"),
        # 翻译文件 (源: labelme/translate/*.qm -> 目标: translate)
        (str(LABELME_ROOT / "translate" / "*.qm"), "translate"),
        # OSAM必要的词汇表文件
        (str(OSAM_PATH / "_models" / "yoloworld" / "clip" / "bpe_simple_vocab_16e6.txt.gz"),
         "osam/_models/yoloworld/clip"),
    ],
    hiddenimports=[
        "osam",
        "osam._models",
        "osam._models.yoloworld",
        "osam._models.yoloworld.clip"
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='labelme',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,  # 保持控制台输出以便调试
    icon=str(LABELME_ROOT / "icons" / "icon.ico"),  # 图标路径
)
