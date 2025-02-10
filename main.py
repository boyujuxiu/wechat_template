import click
import os
from src.converter import MarkdownConverter

@click.command()
@click.option('--input-dir', '-i', required=True, help='输入Markdown文件夹路径')
@click.option('--output-dir', '-o', required=True, help='输出HTML文件夹路径')
@click.option('--template-dir', '-t', required=True, help='模板文件夹路径')
def convert(input_dir, output_dir, template_dir):
    """
    将指定目录下的Markdown文件转换为HTML格式的txt文件
    
    示例:
    python main.py -i ./markdown文件夹 -o ./输出文件夹 -t ./模板文件夹
    """
    try:
        # 验证目录是否存在
        if not os.path.exists(input_dir):
            raise click.BadParameter(f"输入目录不存在: {input_dir}")
        if not os.path.exists(template_dir):
            raise click.BadParameter(f"模板目录不存在: {template_dir}")
            
        # 创建转换器
        converter = MarkdownConverter(template_dir)
        
        # 开始转换
        click.echo("开始转换...")
        success_count, fail_count = converter.convert_directory(input_dir, output_dir)
        
        # 输出结果
        click.echo(f"\n转换完成!")
        click.echo(f"成功: {success_count} 个文件")
        click.echo(f"失败: {fail_count} 个文件")
        
        if fail_count > 0:
            click.echo("\n请检查错误信息并重试失败的文件")
            
    except Exception as e:
        click.echo(f"发生错误: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    convert() 