FROM python:3.7-alpine

ADD usersim/ /usersim

WORKDIR /usersim
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "usersim.py"]