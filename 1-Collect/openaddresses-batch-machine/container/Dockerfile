FROM alpine:3.11

ENV BATCH_MACHINE_PATH=/batch-machine

RUN apk add nodejs yarn git python3 python3-dev py3-pip \
    py3-gdal gdal gdal-dev make bash sqlite-dev zlib-dev \
    postgresql-libs gcc g++ musl-dev postgresql-dev cairo \
    py3-cairo file

# Download and install Tippecanoe
RUN git clone -b 1.35.0 https://github.com/mapbox/tippecanoe.git /tmp/tippecanoe && \
    cd /tmp/tippecanoe && \
    make && \
    PREFIX=/usr/local make install && \
    rm -rf /tmp/tippecanoe

# Get/install batch-machine
RUN git clone https://github.com/JosephKuchar/batch-machine $BATCH_MACHINE_PATH && \
	pip3 install $BATCH_MACHINE_PATH

# Restrict to non-root access
RUN addgroup appgroup && \
	adduser -S -g appgroup appuser
USER appuser

CMD python3 ${BATCH_MACHINE_PATH}/test.py
