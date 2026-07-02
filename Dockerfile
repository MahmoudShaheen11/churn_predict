FROM python:3.10

WORKDIR /app

# نسخ الملفات
COPY . /app

# تثبيت المكتبات
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# فتح البورت
EXPOSE 8501

# تشغيل Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]