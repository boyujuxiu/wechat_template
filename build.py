import PyInstaller.__main__
import os

def build_exe():
    # 确保dist目录存在
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # 复制模板文件到dist目录
    if os.path.exists('templates'):
        os.system('xcopy templates dist\\templates /E /I /H /Y')
    
    # PyInstaller参数
    params = [
        'gui.py',  # 主程序文件
        '--name=Markdown转HTML工具',  # 生成的exe名称
        '--windowed',  # 使用GUI模式
        '--onefile',  # 打包成单个exe文件
        '--icon=icon.ico',  # 如果有图标的话
        '--add-data=src;src',  # 添加源代码目录
        '--noconfirm',  # 覆盖现有文件
        '--clean',  # 清理临时文件
    ]
    
    # 运行PyInstaller
    PyInstaller.__main__.run(params)

if __name__ == '__main__':
    build_exe() 