FROM python:3
RUN touch /tmp/access.log
WORKDIR /usr/src
ADD ./dd_homework /usr/src
ADD ./requirement.txt /usr/src
ADD ./Makefile /usr/src
RUN make install
ENTRYPOINT ["python", "main.py"]