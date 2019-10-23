FROM postgres:11.1

RUN apt-get update -yqq && \
    apt-get install -yqq wget build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev  libncursesw5-dev xz-utils tk-dev && \
    wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz && \
    tar xvf Python-3.6.9.tgz && \
    cd Python-3.6.9 && \
    ./configure --enable-optimizations --enable-shared --with-ensurepip=install && \
    make -j8 && \
    make altinstall

RUN apt-get install -yqq postgresql-server-dev-11 git

COPY . /s3_fdw/
WORKDIR /s3_fdw

RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.6 1 && \
    rm /usr/bin/lsb_release

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install virtualenv


ENV VIRTUAL_ENV=/s3_fdw/venv
RUN python3 -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt && \
    pip install .

RUN git clone git://github.com/Kozea/Multicorn.git && \
    cd Multicorn && \
    git checkout 9ff78759665b0d04315f707b81a45c66ecb2d8c7 && \
    make && make install