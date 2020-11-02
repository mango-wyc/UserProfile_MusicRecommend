FROM python:3.7

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code

# 更新 pip
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
# 设置清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /code/

# 安装库
RUN pip install -r requirements.txt

# 将当前目录复制到容器的 code 目录
ADD . /code/