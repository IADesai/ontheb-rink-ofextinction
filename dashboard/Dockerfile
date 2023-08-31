FROM python

EXPOSE 8501

WORKDIR /dashboard

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY extract_s3.py .

COPY streamlit_app.py .

COPY pipeline.py .

CMD ["streamlit", "run", "pipeline.py"]