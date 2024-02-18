## Dockerfile
FROM python:3.9.16

# 更新apt-get
RUN apt-get update -y 

# 改成台北時區
RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

# 更新pip
RUN pip install --upgrade pip

# 載入專案與安裝套件
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

CMD tail -f /dev/null