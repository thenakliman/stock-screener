FROM python:3.9-slim AS builder
WORKDIR /app
COPY . ./
RUN python setup.py bdist_wheel

FROM python:3.9-slim
RUN useradd -ms /bin/bash screener
USER screener
WORKDIR /home/screener
ENV PATH=${PATH}:/home/screener/.local/bin
COPY --from=builder /app/dist/screener-0.0.1-py3-none-any.whl .
RUN pip install screener-0.0.1-py3-none-any.whl
CMD screener
