FROM apache/airflow:2.3.0

# Install dbt
RUN pip install -U pip
RUN pip install dbt-postgres
RUN pip install --upgrade Jinja2==3.0.3

# Expose port for dbt docs
EXPOSE 8080

CMD ["scheduler"]