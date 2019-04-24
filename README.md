# A-Smart-Photo-Album
智能相册
## 设计思路：
使用python的多进程进行预测，协程进行下载，多个进程和请求分发器之间使用了socket通信（sockpair)。
图像检测识别使用了Image AI库:<a href="https://github.com/OlafenwaMoses/ImageAI">ImageAI</a>
## 主要的文件：
1.Interface/Observer.py
多进程和协程执行检测程序的文件
2.Interface/views.py
处理url，分发检测请求给多个Observer进程中最空闲的一个，保证并发请求能及时响应
