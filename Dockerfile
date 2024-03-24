FROM python:3.11.4
ENV PYTHONBUFFERED 1
WORKDIR /
COPY . /
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python", "S_Predictor/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
