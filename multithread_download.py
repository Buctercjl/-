import requests
from concurrent.futures import ThreadPoolExecutor
import os

def download_file(url, filename):
    try:
        response = requests.get(url, timeout=10, verify=True)  # 临时禁用SSL验证（不安全，仅用于测试）
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    urls = [
        "",  # 示例URL，请替换为实际下载链接
        # 添加更多URL
    ]
    os.makedirs('downloads', exist_ok=True)
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(download_file, url, f"downloads/file{i}{os.path.splitext(url)[1]}") for i, url in enumerate(urls)]
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()