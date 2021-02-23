# TA-LIB with BITFLYER

## 使うパッケージのインストールについて  
windows の場合は以下でインストール  
```
pip install pipenv
pipenv install
```

linux の場合、ta-lib だけインストールは以下のコマンドでインストール
```
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -zxvf ta-lib-0.4.0-src.tar.gz && \
cd ta-lib && \
./configure --prefix=/usr && \
make && \
make install && \
cd .. && \
rm -rf ta-lib-0.4.0-src.tar.gz && rm -rf ta-lib
pip install TA-LIB
```
ラズベリーパイの場合、numpy とpandas が上手くインストールできないので、python3-numpy とpython3-pandasをapt-getでインストールしてください。

## 実際に動かしてみる場合
実際に動かしてみたい場合は、manage.pyのあるディレクトリに移動して、以下のコマンドを実行してください。
```
python manage.py makemigrations
python manage.py migrate
python manage.py startstream
```