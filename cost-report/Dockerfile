FROM public.ecr.aws/lambda/python:3.12

COPY ./requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY cost_report_prod.py ${LAMBDA_TASK_ROOT}
EXPOSE 8080
CMD ["cost_report_prod.lambda_handler"]