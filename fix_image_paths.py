import os
import re

# 根目录路径
root_dir = os.path.abspath('.')

# 要排除的文件
exclude_files = ['README.md']

# 遍历所有子目录
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 排除根目录
    if dirpath == root_dir:
        continue
    
    # 处理每个目录中的markdown文件
    for filename in filenames:
        if filename.endswith('.md') and filename not in exclude_files:
            file_path = os.path.join(dirpath, filename)
            
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 是否有修改
                modified = False
                
                # 匹配更多可能的模式
                patterns = [
                    # 标准Markdown图片引用
                    (r'!\[(.*?)\]\(\.\/images\/', r'![\1](../images/'),
                    (r'!\[\]\(\.\/images\/', r'![](../images/'),
                    # 直接引用./images路径（非Markdown语法）
                    (r'[\'"](\.\/images\/)', r'"../images/'),
                    (r'[^\(]\.\/images\/', r'../images/'),
                    # HTML img标签中的路径
                    (r'<img\s+src=["\']\.\/images\/', r'<img src="../images/'),
                    # JSON字符串中的路径
                    (r'(content.*?)\.\/images\/', r'\1../images/'),
                    # 变量赋值中的路径
                    (r'(=\s*["\'])\.\/images\/', r'\1../images/')
                ]
                
                # 应用所有模式
                for pattern, replacement in patterns:
                    new_content = re.sub(pattern, replacement, content)
                    if new_content != content:
                        content = new_content
                        modified = True
                        print(f"  在 {file_path} 中匹配到模式 {pattern}")
                
                # 如果有修改，写回文件
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"已修改: {file_path}")
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")

print("所有文件处理完成！") 