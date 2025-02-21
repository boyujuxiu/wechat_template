# Markdown转HTML工具

这是一个将Markdown文件批量转换为HTML格式（保存为txt文件）的Python工具。它支持自定义模板，可以为二级标题添加特定样式，并且可以为加粗文本设置特定颜色。

## 功能特点

- 图形界面操作，简单易用
- 批量转换指定目录下的所有Markdown文件
- 支持自定义输出目录
- 支持模板系统，可自定义页面顶部和底部内容
- 支持二级标题样式自定义
- 支持加粗文本颜色自定义（通过模板目录中的boldcolor.txt文件）
- 自动在二级标题前添加空行，优化排版
- 自动保存配置，记住上次设置
- 实时转换进度显示
- 详细的操作日志记录
- 苹果风格界面设计
- 支持多级模板目录结构

## 技术选型说明

在开发过程中，我们经历了以下技术选型的考虑：

1. 最初考虑使用命令行界面，但为了提供更好的用户体验，改为图形界面实现
2. GUI框架选择过程：
   - 首先尝试使用 PyQt6，但遇到了 DLL 加载问题
   - 然后尝试使用 PySide6，但同样遇到了依赖问题
   - 最终选择使用 Python 内置的 tkinter，具有以下优势：
     * 无需额外安装依赖
     * 跨平台兼容性好
     * 足够轻量级
     * 适合简单的工具类应用

## 安装方式

### 方式一：直接使用exe程序（推荐）
1. 下载发布页面的最新版本exe文件
2. 双击运行即可使用

### 方式二：从源码运行
1. 克隆本仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```
3. 运行程序：
```bash
python gui.py
```

## 使用方法

1. 运行程序后，您会看到一个分为左右两栏的图形界面：
   - 左侧为配置区域，用于选择目录和控制转换
   - 右侧为日志区域，显示实时操作记录

2. 设置工作目录：
   - 点击对应的"选择"按钮选择目录
   - 程序会自动记住上次的设置

3. 选择必要的目录：
   - 输入目录（包含Markdown文件的目录）
   - 输出目录（转换后文件的保存位置）
   - 模板目录（包含模板文件的目录）

4. 模板目录结构说明：
   - 选择的模板目录应该包含一个或多个子文件夹
   - 每个子文件夹可以是一个独立的模板集
   - 程序会自动在子文件夹中查找所需的模板文件
   - 使用第一个包含完整模板文件集的子文件夹

5. 模板目录示例：
   ```
   模板父目录/
   ├── 模板1/
   │   ├── top.html
   │   ├── bottom.html
   │   ├── h2.html
   │   └── boldcolor.txt
   ├── 模板2/
   │   ├── top.html
   │   ├── bottom.html
   │   ├── h2.html
   │   └── boldcolor.txt
   └── 其他子文件夹/
   ```

6. 点击"开始转换"按钮开始转换

7. 转换过程中可以：
   - 查看实时进度条
   - 查看当前处理的文件名
   - 在日志区域查看详细的转换记录
   - 使用清除日志按钮清空日志记录

## 模板文件要求

模板目录中的子文件夹需要包含以下文件：
- `top.html`：将被插入到每个转换后文件的顶部
- `bottom.html`：将被插入到每个转换后文件的底部
- `h2.html`：用于二级标题的样式模板，使用 `{h2_text}` 作为标题文本的占位符
- `boldcolor.txt`：指定加粗文本的颜色，内容为颜色代码（如 '#E7C60A'）。如果文件不存在，将使用默认颜色 '#ff6827'

## 界面设计

1. 整体风格：
   - 采用苹果风格设计
   - 简洁现代的界面布局
   - 清晰的视觉层次

2. 配色方案：
   - 浅灰色背景 (#f5f5f7)
   - 主按钮使用苹果蓝 (#0066cc)
   - 次要按钮使用白底蓝边
   - 统一的颜色搭配

3. 控件样式：
   - 扁平化设计
   - 圆角进度条
   - 无边框文本框
   - 合理的间距和留白
   - 主次按钮样式区分

4. 字体设计：
   - 默认使用苹果系统字体 (SF Pro Display)
   - 合适的字体大小和粗细
   - 清晰的文字层级

## 按钮设计

1. 主按钮（如"开始转换"）：
   - 蓝色背景 (#0066cc)
   - 白色文字
   - 悬停时颜色加深 (#0077ed)
   - 较大内边距 (20, 8)

2. 次要按钮（如"选择"、"清除日志"）：
   - 白色背景
   - 蓝色边框和文字
   - 悬停时背景变浅灰 (#f5f5f7)
   - 适中内边距 (15, 6)

3. 按钮布局：
   - 使用专门的按钮容器
   - 统一的对齐方式
   - 自适应宽度
   - 合理的间距

## 样式说明

1. 段落样式：
   - 使用微软雅黑字体
   - 设置了合适的段落间距和行高
   - 统一的字间距

2. 二级标题样式：
   - 支持自定义模板（h2.html）
   - 自动添加空行优化排版
   - 支持标题序号自动递增（使用 {h2_count} 占位符）
   - 智能空行处理（避免重复添加空行）
   - 支持复杂的HTML结构（如多层section嵌套）

3. 加粗文本样式：
   - 颜色从 `boldcolor.txt` 文件读取
   - 白色背景
   - 微软雅黑字体

4. 图片处理：
   - 每个图片后自动添加换行
   - 保持原始图片属性

## 模板文件说明

### h2.html 模板示例
```html
<section class="_editor" data-style-id="49165" data-type="undefined" data-id="49165" data-vip="3" data-free="0">
    <section data-align="title" style="display:flex;margin:10px 0px;justify-content:center;align-items:center;" class="">
        <section style="width:25px;height:25px;border-radius:50%;background-color:#fee13c;text-align:center;transform:rotate(0deg);margin-right:10px;">
            <section style="font-sizE:14px;line-height:25px;">
                <p>
                    <b><i>{h2_count}</i></b>
                </p>
            </section>
        </section>
        <section style="background-color:#f3fbf7;padding:5px 40px;border-radius:30px;">
            <section style="font-size:16px;letter-spacing:2px;">
                <p>
                    <strong>{h2_text}</strong>
                </p>
            </section>
        </section>
    </section>
</section>
```

模板中的占位符说明：
- `{h2_text}`: 二级标题的文本内容
- `{h2_count}`: 自动递增的标题序号（从1开始）

### 空行处理说明
程序会在每个二级标题前自动添加空行，使用以下HTML结构：
```html
<p class="aiActive"><br/></p>
```

空行处理的特点：
1. 智能检测：如果标题前已有空行，不会重复添加
2. 统一格式：使用HTML标签确保空行显示一致
3. 支持自定义样式：可以通过CSS类 `aiActive` 控制空行样式
4. 兼容性好：适用于各种HTML渲染环境

## 开发者信息

### 项目依赖
项目使用了以下主要依赖：
```
markdown==3.4.1    # 用于Markdown到HTML的转换
Jinja2==3.1.2      # 用于模板处理
pyinstaller==6.3.0 # 用于打包exe程序
```

### 打包程序

如果您想自己打包程序，可以使用以下命令：

```bash
pyinstaller --name="Markdown转HTML工具" --windowed --onefile --add-data "src;src" gui.py
```

打包后的程序将在 `dist` 目录中生成。

### 项目结构
```
markdown_converter/
├── src/
│   ├── __init__.py
│   └── converter.py     # 核心转换逻辑
├── gui.py              # 图形界面实现
├── requirements.txt    # 项目依赖
└── README.md          # 项目说明
```

## 注意事项

1. 确保模板目录中包含所有必需的模板文件
2. 输入目录中的文件必须是 .md 或 .markdown 格式
3. 转换后的文件将保存为 .txt 格式
4. 如果输出目录不存在，程序会自动创建
5. 程序会自动保存您的配置，下次启动时自动加载

## 常见问题解决

1. 如果运行时遇到 "DLL load failed" 错误，请确保：
   - 已安装最新版本的 Python
   - 系统已安装必要的 Visual C++ 运行库

2. 如果打包时遇到问题，可以尝试：
   - 使用管理员权限运行命令提示符
   - 确保所有依赖都已正确安装
   - 使用 `--clean` 参数重新打包 

## 已知问题及解决方案

### 1. 段落样式问题

**问题描述：**
在早期版本中，程序会为所有段落（包括标题段落）添加统一的样式，这导致了二级标题的显示出现异常，出现了多余的样式属性。

**解决方案：**
- 移除了对所有段落统一添加样式的处理
- 让二级标题的样式完全由模板文件(h2.html)控制
- 普通段落的样式可以通过模板文件(top.html)中的CSS来控制

**代码修改：**
```python
class CustomMarkdownConverter(markdown.Markdown):
    def convert(self, source):
        try:
            source = re.sub(r'\*\* +', '**', source)  # 删除**后的空格
            source = re.sub(r' +\*\*', '**', source)  # 删除**前的空格
            
            html = super().convert(source)
            # 移除统一的段落样式
            return html
        except Exception as e:
            print(f"Markdown转换出错: {str(e)}")
            raise
```

**使用建议：**
1. 如需自定义段落样式，请在模板文件中通过CSS来实现
2. 二级标题的样式应该在h2.html模板中定义
3. 通用样式可以在top.html中通过CSS统一设置 