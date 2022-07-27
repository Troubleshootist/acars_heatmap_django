import subprocess
import jinja2
import os
from jinja2 import Template
from django.conf import settings
from django.db.models import Sum    

from .models import *

LATEX_JINJA_ENV = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.join(settings.MEDIA_ROOT, 'tex'))
)


def task_card_print(pk):
    task_card = TaskCard.objects.get(pk=pk)
    template = LATEX_JINJA_ENV.get_template('task_card_template.tex')
    context = {
        'task_card': task_card,
        'number': task_card.number,
        'description': task_card.description,
        'ac_type': task_card.plane_type.type,
        'defect_ref': task_card.defect.reference if task_card.defect else 'N/A',
        'down_time': task_card.steps.aggregate(sum=Sum('manhours'))['sum']
    }
    print(template.render(context))
    document = template.render(context)

    with open(os.path.join(settings.MEDIA_ROOT, 'tex', 'output', task_card.number + '.tex'), 'w') as output:
        output.seek(0)
        document = document.replace('#', '''\#''')

        output.write(document)
        output.close
    latex_code = subprocess.call('/usr/local/texlive/2022/bin/x86_64-linux/pdflatex -output-directory=' + os.path.join(settings.MEDIA_ROOT, 'tex', 'output') + ' ' + output.name, shell=True)
    if latex_code != 0:
        print('problem')
    return os.path.join(settings.MEDIA_ROOT, 'tex', 'output', task_card.number + '.pdf')

