FROM python:latest
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD src /ssks/
RUN adduser python
WORKDIR /ssks/
RUN mkdir /ssks-data
VOLUME ["/ssks-data"]
EXPOSE 8000
CMD ["uvicorn", "sealdsdkstorage:app", "--host", "0.0.0.0"]