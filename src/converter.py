import re
import os
import markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor
from jinja2 import Template, FileSystemLoader, Environment

class BoldColorPattern(SimpleTagInlineProcessor):
    def handleMatch(self, m, data):
        el = super().handleMatch(m, data)[0]
        el.set('style', 'color: #af2618;')  # 设置加粗文本的颜色
        return el, m.start(0), m.end(0)

class BoldColorExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # 注册加粗文本处理器
        pattern = BoldColorPattern(r'\*\*([^*]+)\*\*', 'strong')
        md.inlinePatterns.register(pattern, 'boldcolor', 175)

class MarkdownConverter:
    def __init__(self, template_dir):
        self.template_dir = template_dir
        self.md = markdown.Markdown(extensions=[BoldColorExtension()])
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
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
        h2_pattern = re.compile(r'## (.*?)\n')
        
        def replace_h2(match):
            h2_text = match.group(1)
            return self.h2_template.replace('{h2_text}', h2_text)
        
        return h2_pattern.sub(replace_h2, content)

    def convert_file(self, input_file, output_file):
        """转换单个文件"""
        try:
            # 读取markdown内容
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 处理二级标题
            content = self._process_h2_titles(content)
            
            # 转换markdown到HTML
            html_content = self.md.convert(content)
            
            # 组合最终内容
            final_content = self.top_template + html_content + self.bottom_template
            
            # 保存为txt文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
                
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