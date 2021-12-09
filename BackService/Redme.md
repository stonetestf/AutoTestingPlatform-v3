# 部署说明
## 环境安装
### 安装Python依赖
    1. 安装python310环境
    2. pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-dependencies


## 环境安装可能错误处理：
### 安装mysqlcen错误处理
    yum install mysql-devel gcc gcc-devel python-devel
    pip3 install mysqlclient


# 运行说明
    /usr/local/nginx/sbin/nginx


# 平台说明
##接口维护
    1.接口中的前置操作,会在接口运行前运行
    2.接口中的后置操作,只会在接口运行完成后进行!