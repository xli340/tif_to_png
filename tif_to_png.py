import os
from PIL import Image
import glob

def convert_tif_to_png():
    """
    将当前路径下的所有TIF文件转换为PNG格式，保存到新建的文件夹中
    """
    # 获取当前工作目录
    current_dir = os.getcwd()
    current_folder_name = os.path.basename(current_dir)
    
    print(f"当前工作目录: {current_dir}")
    print(f"当前文件夹名: {current_folder_name}")
    
    # 创建输出文件夹
    output_folder = os.path.join(current_dir, f"{current_folder_name}_png")
    print(f"输出文件夹路径: {output_folder}")
    
    try:
        os.makedirs(output_folder, exist_ok=True)
        print(f"输出文件夹创建成功")
    except Exception as e:
        print(f"创建输出文件夹失败: {e}")
        return
    
    # 查找所有TIF文件 - 修复：使用os.listdir而不是glob
    all_files = os.listdir(current_dir)
    tif_files = []
    
    for file in all_files:
        if file.lower().endswith(('.tif', '.tiff')):
            full_path = os.path.join(current_dir, file)
            # 确保不是目录，且不在输出文件夹中
            if os.path.isfile(full_path) and not full_path.startswith(output_folder):
                tif_files.append(full_path)
    
    print(f"找到的TIF文件: {len(tif_files)}")
    for i, file in enumerate(tif_files):
        print(f"  {i+1}. {os.path.basename(file)}")
    
    if not tif_files:
        print("没有找到TIF文件！")
        return
    
    # 按文件名排序
    tif_files.sort()
    
    # 转换文件
    converted_count = 0
    
    for i, tif_file in enumerate(tif_files, 1):
        try:
            print(f"\n正在处理第 {i} 个文件: {os.path.basename(tif_file)}")
            
            # 打开TIF文件
            with Image.open(tif_file) as img:
                print(f"  图像模式: {img.mode}, 尺寸: {img.size}")
                
                # 构建输出文件名
                png_filename = f"{current_folder_name}_{i:03d}.png"
                png_filepath = os.path.join(output_folder, png_filename)
                
                print(f"  输出文件: {png_filename}")
                
                # 转换并保存
                if img.mode in ['RGBA', 'LA']:
                    img.save(png_filepath, "PNG")
                else:
                    rgb_img = img.convert('RGB')
                    rgb_img.save(png_filepath, "PNG")
                
                # 验证文件是否创建成功
                if os.path.exists(png_filepath):
                    file_size = os.path.getsize(png_filepath)
                    print(f"  ✓ 转换成功! 文件大小: {file_size} bytes")
                    converted_count += 1
                else:
                    print(f"  ✗ 转换失败! 文件未创建")
                    
        except Exception as e:
            print(f"  ✗ 转换 {os.path.basename(tif_file)} 时出错: {str(e)}")
    
    print(f"\n=== 转换完成 ===")
    print(f"共转换了 {converted_count} 个文件")
    print(f"输出文件夹: {output_folder}")
    
    # 验证输出文件夹中的文件
    try:
        output_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]
        print(f"输出文件夹中的PNG文件数量: {len(output_files)}")
        for file in sorted(output_files):
            print(f"  - {file}")
    except Exception as e:
        print(f"检查输出文件夹时出错: {e}")

if __name__ == "__main__":
    convert_tif_to_png()