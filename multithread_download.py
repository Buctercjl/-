import requests
from concurrent.futures import ThreadPoolExecutor
import os

def download_chunk(url, chunk_start, chunk_end, save_path):
    """下载文件的指定分片块"""
    headers = {'Range': f'bytes={chunk_start}-{chunk_end}'}
    resp = requests.get(url, headers=headers, timeout=30)
    # 将下载的分片写入文件对应位置
    with open(save_path, 'r+b') as f:
        f.seek(chunk_start)
        f.write(resp.content)
    return f"Finished chunk {chunk_start}-{chunk_end}"

def multi_thread_download(url, save_path, num_threads=8):
    """多线程下载主函数"""
    # 1. 获取文件总大小
    resp_head = requests.head(url)
    total_size = int(resp_head.headers.get('Content-Length', 0))
    if total_size == 0:
        raise ValueError("无法获取文件大小，该链接不支持分片下载")
    
    # 2. 创建空文件预占空间

    # ===== 添加目录自动创建逻辑 =====
    save_dir = os.path.dirname(save_path)
    # 如果保存目录不为空且不存在，自动创建
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    # 原来的创建文件代码不变    
    with open(save_path, 'wb') as f:
        f.truncate(total_size)
    
    # 3. 计算每个线程负责的分片范围
    chunk_size = total_size // num_threads
    chunks = []
    for i in range(num_threads):
        start = i * chunk_size
        end = (i+1) * chunk_size - 1 if i != num_threads-1 else total_size - 1
        chunks.append((start, end))
    
    # 4. 启动多线程下载
    with ThreadPoolExecutor(max_workers=num_threads) as pool:
        futures = [
            pool.submit(download_chunk, url, start, end, save_path)
            for start, end in chunks
        ]
        for future in futures:
            print(future.result())
    
    print(f"\n下载完成！文件保存至：{os.path.abspath(save_path)}")


# -------- 调用示例 --------
if __name__ == "__main__":
    # 替换为你需要下载的文件链接
    target_url = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi" 
    # 替换为你的保存路径和文件名
    save_file = "downloads\wsl_update_x64.msi" 
    multi_thread_download(target_url, save_file, num_threads=8)
