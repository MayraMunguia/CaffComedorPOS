# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_order_totalcompra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='nombre',
            field=models.CharField(max_length=100, blank=True, null=True, default='Invitado'),
        ),
    ]
