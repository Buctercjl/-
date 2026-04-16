# 多线程下载

这是一个简单的多线程文件下载器，使用Python编写。

## 使用方法

1. 安装依赖：`pip install -r requirements.txt`

2. 编辑 `multithread_download.py` 中的 `urls` 列表，添加要下载的文件URL。

3. 运行：`python multithread_download.py`

## 注意

- 确保URL是有效的。
- 下载的文件保存在 `downloads` 文件夹中。
- 脚本使用4个线程并发下载，可以根据需要调整 `max_workers`。

## 故障排除

- 如果遇到网络错误，请检查URL和网络连接。
- 如果缺少模块，请确保安装了requirements.txt中的依赖。
