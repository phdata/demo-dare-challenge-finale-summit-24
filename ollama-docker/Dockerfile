FROM  --platform=linux/amd64 ollama/ollama

# INSTALL DEPENDENCIES
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    wget sudo git bzip2 python3 ca-certificates \
    xterm \
    python-is-python3\
    python3-pip

RUN python3 -m pip install flask numpy jupyterlab snowflake streamlit

RUN mkdir src
RUN mkdir src/app
COPY entrypoint.sh /src/
COPY app/main.py /src/app/

ENTRYPOINT ["/src/entrypoint.sh"]
