import re
import os
import markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor, ImageInlineProcessor
from jinja2 import Template, FileSystemLoader, Environment
try:
    from markdown.util import etree
except ImportError:
    try:
        from xml.etree import ElementTree as etree
    except ImportError:
        from xml.etree import cElementTree as etree

class BoldColorPattern(SimpleTagInlineProcessor):
    def __init__(self, pattern, md, bold_color):
        # 不调用父类的初始化方法，直接自己实现
        self.pattern = pattern
        self.md = md
        self.bold_color = bold_color
        # 编译正则表达式
        self.compiled_re = re.compile(pattern)

    def handleMatch(self, m, data):
        try:
            # 直接创建 strong 元素，使用正确的 etree
            el = etree.Element('strong')
            # 设置文本内容
            el.text = m.group(1) if m and m.group(1) else ''
            # 设置样式
            el.set('style', f'color: {self.bold_color}; background-color: #ffffff; font-family: 微软雅黑, "Microsoft YaHei";')
            return el, m.start(0), m.end(0)
        except Exception as e:
            print(f"处理加粗文本时出错: {str(e)}")
            return None, None, None

class CustomImagePattern(ImageInlineProcessor):
    def handleMatch(self, m, data):
        el, start, end = super().handleMatch(m, data)
        if el is not None:
            br = etree.Element('br')
            parent = etree.Element('div')
            parent.append(el)
            parent.append(br)
            return parent, start, end
        return el, start, end

class BoldColorExtension(markdown.Extension):
    def __init__(self, **kwargs):
        self.bold_color = kwargs.pop('bold_color', '#ff6827')  # 默认颜色
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        # 删除原有的加粗处理器
        if 'strong' in md.inlinePatterns:
            del md.inlinePatterns['strong']
        
        # 使用更简单的正则表达式
        pattern = r'\*\*(.+?)\*\*'
        bold_pattern = BoldColorPattern(pattern, md, self.bold_color)
        md.inlinePatterns.register(bold_pattern, 'strong', 175)

        # 替换默认的图片处理器
        if 'image' in md.inlinePatterns:
            del md.inlinePatterns['image']
        image_pattern = CustomImagePattern(markdown.inlinepatterns.IMAGE_LINK_RE, md)
        md.inlinePatterns.register(image_pattern, 'image', 150)

class CustomMarkdownConverter(markdown.Markdown):
    def convert(self, source):
        try:
            # 预处理 markdown 内容，确保加粗语法正确
            source = re.sub(r'\*\* +', '**', source)  # 删除**后的空格
            source = re.sub(r' +\*\*', '**', source)  # 删除**前的空格
            
            html = super().convert(source)
            # 修改这里：不要为所有段落添加样式
            # html = html.replace('<p>', '<p style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; margin-top: 20px; margin-bottom: 32px; line-height: 1.75em;">')
            return html
        except Exception as e:
            print(f"Markdown转换出错: {str(e)}")
            raise

class MarkdownConverter:
    def __init__(self, template_dir):
        self.template_dir = template_dir
        # 读取加粗文字颜色
        try:
            with open(os.path.join(template_dir, 'boldcolor.txt'), 'r', encoding='utf-8') as f:
                bold_color = f.read().strip()
        except FileNotFoundError:
            bold_color = '#ff6827'  # 默认颜色
            
        self.md = CustomMarkdownConverter(extensions=[BoldColorExtension(bold_color=bold_color)])
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # 初始化二级标题计数器
        self.h2_count = 0
        
        # 加载模板
        self._load_templates()

    def _load_templates(self):
        """加载所有必要的模板"""
        try:
            with open(os.path.join(self.template_dir, 'top.html'), 'r', encoding='utf-8') as f:
                self.top_template = f.read()
            with open(os.path.join(self.template_dir, 'bottom.html'), 'r', encoding='utf-8') as f:
                self.bottom_template = f.read()
            with open(os.path.join(self.template_dir, 'h2.html'), 'r', encoding='utf-8') as f:
                self.h2_template = f.read()
        except FileNotFoundError as e:
            raise Exception(f"模板文件未找到: {str(e)}")

    def _process_h2_titles(self, content):
        """处理二级标题，应用h2模板"""
        try:
            # 重置计数器
            self.h2_count = 0
            
            # 先将内容按行分割
            lines = content.split('\n')
            processed_lines = []
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('## '):
                    # 增加计数器
                    self.h2_count += 1
                    h2_text = line[3:].strip()  # 去掉'## '和两端空白
                    
                    # 检查前面是否已经有空行或br标签
                    has_space = False
                    if processed_lines:
                        last_line = processed_lines[-1].strip()
                        if (last_line == '' or 
                            last_line == '<br/>' or 
                            last_line == '</p>' or 
                            '<p class="aiActive">' in last_line):
                            has_space = True
                    
                    # 只在没有空行时添加空行和br标签
                    if not has_space:
                        processed_lines.append('<p class="aiActive">')
                        processed_lines.append('    <br/>')
                        processed_lines.append('</p>')
                    
                    if not self.h2_template:
                        print("警告: h2模板为空")
                        processed_lines.append(f"<h2>{h2_text}</h2>")
                    else:
                        # 确保模板中的换行符被正确处理
                        template = self.h2_template.replace('\n', '').strip()
                        # 使用安全的字符串替换，同时替换 h2_text 和 h2_count
                        result = template.replace('{h2_text}', h2_text).replace('{h2_count}', str(self.h2_count))
                        processed_lines.append(result)
                else:
                    processed_lines.append(lines[i])
                i += 1
            
            # 重新组合内容
            return '\n'.join(processed_lines)
        except Exception as e:
            print(f"处理标题时出错: {str(e)}")
            return content  # 返回原始内容

    def convert_file(self, input_file, output_file):
        """转换单个文件"""
        try:
            # 读取markdown内容
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 先转换markdown到HTML
            try:
                html_content = self.md.convert(content)
            except Exception as e:
                print(f"Markdown转换时出错: {str(e)}")
                raise
            
            # 处理二级标题和添加空行
            try:
                # 使用正则表达式匹配二级标题的HTML标签
                h2_pattern = re.compile(r'(?:<h2>|<section[^>]*?>\s*<section[^>]*?>\s*<section[^>]*?>\s*<p>\s*<strong>)(.*?)(?:</h2>|</strong></p>\s*</section>\s*</section>\s*</section>)', re.DOTALL)
                
                def replace_h2(match):
                    self.h2_count += 1
                    h2_text = match.group(1).strip()
                    
                    if not self.h2_template:
                        return f'<p class="aiActive"><br/></p>\n<h2>{h2_text}</h2>'
                    
                    template = self.h2_template.replace('\n', '').strip()
                    result = template.replace('{h2_text}', h2_text).replace('{h2_count}', str(self.h2_count))
                    return f'<p class="aiActive"><br/></p>\n{result}'
                
                # 重置计数器
                self.h2_count = 0
                html_content = h2_pattern.sub(replace_h2, html_content)
                
            except Exception as e:
                print(f"处理标题时出错: {str(e)}")
            
            # 组合最终内容
            try:
                final_content = self.top_template + html_content + self.bottom_template
            except Exception as e:
                print(f"组合内容时出错: {str(e)}")
                raise
            
            # 保存为txt文件
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)
            except Exception as e:
                print(f"保存文件时出错: {str(e)}")
                raise
                
            return True
        except Exception as e:
            print(f"转换文件 {input_file} 时出错: {str(e)}")
            return False

    def convert_directory(self, input_dir, output_dir, progress_callback=None):
        """转换整个目录下的markdown文件
        
        Args:
            input_dir: 输入目录路径
            output_dir: 输出目录路径
            progress_callback: 进度回调函数，接收参数：(当前进度, 总文件数, 当前文件名)
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        success_count = 0
        fail_count = 0
        
        # 获取所有要处理的文件
        md_files = [f for f in os.listdir(input_dir) if f.endswith(('.md', '.markdown'))]
        total_files = len(md_files)
        
        for index, filename in enumerate(md_files, 1):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, 
                                     os.path.splitext(filename)[0] + '.txt')
            
            if self.convert_file(input_path, output_path):
                success_count += 1
            else:
                fail_count += 1
            
            if progress_callback:
                progress_callback(index, total_files, filename)
        
        return success_count, fail_count 