FROM odoo:18.0

COPY ./requirements.txt /etc/odoo/requirements.txt

USER root
RUN pip install --no-cache-dir --break-system-packages -r /etc/odoo/requirements.txt
USER odoo
