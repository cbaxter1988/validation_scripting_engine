FROM cbaxter1988/vse:base

COPY dist /

RUN tar -xzf /vse-1.0.tar.gz && cd VSE-1.0 && python setup.py install

ENTRYPOINT  ["python3", "-m", "vse"]

CMD ["--serve_rpc"]