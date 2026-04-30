ARG BASE_IMAGE
FROM $BASE_IMAGE

RUN pip install auditwheel cmake

COPY . /project
WORKDIR /project

CMD python3 -m pip wheel . --no-deps -w /tmp/wheelhouse && \
    python3 -m auditwheel repair /tmp/wheelhouse/*.whl -w /wheelhouse