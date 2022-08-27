from datetime import datetime, timedelta
import csv
from .models import Employees
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings
import os

def current_date_format(date):
        months = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        day = date.day
        month = months[date.month - 1]
        year = date.year
        messsage = "{} de {} del {}".format(day, month, year)

        return messsage


def csv_to_models(file):
        #Delete database
        Employees.objects.all().delete()   

        reader = csv.reader(file, delimiter = ',')
        next(reader, None)
        for row in reader:
                employees, created = Employees.objects.get_or_create(
                        EMPRESA = row[0],
                        EMPLEADO = row[1],
                        FECHARETIRO = row[2],
                        TOTALSUELDO = row[3],
                        OTROS = row[4],
                        CODCC = row[5],
                        NOMCC = row[6],
                        SEXO = row[7],
                        TIPODOCUMENTO = row[8],
                        NÚMERODEIDENTIFICACIÓN = row[9],
                        CIUDADDOCUMENTO = row[10],
                        FECHADENACIMIENTO = row[11],
                        CIUDADDENACIMIENTO = row[12],
                        FECHADEINGRESO = row[13],
                        CÓDIGOEMPLEDO = row[14],
                        NOMBREDELCARGO = row[15],
                        MOTIVODELCARGO = row[16],
                        NOMBREESTRUCTURACARGO = row[17],
                        DESCRIPCIÓNDELMOTIVO = row[18],
                        VALORSUELDO = row[19],
                        MOTIVOCONTRATO = row[20],
                        TIPODECONTRATO = row[21],
                        NOMBRETIPOTRABAJADOR = row[22],
                        NOMBRETIPOSALARIO = row[23],
                        NOMBRENORMALABORAL = row[24],
                        NOMBRELEGISLACIÓNLABORAL = row[25],
                        UBICACIÓNGEOGRÁFICA = row[26],
                        NOMBREJORNADA = row[27],
                        NOMBREFORMADEPAGO = row[28],
                        CUENTADEPAGO = row[29],
                        TIPOCUENTA = row[30],
                        SUCURSALDEPAGO = row[31],
                        METODODEPAGO = row[32],
                        EPS = row[33],
                        FONDOSDEPENSIONES = row[34],
                        FONDODECESANTÍAS = row[35],
                        RIESGOSPROFESIONALES = row[36],
                        CAJADECOMPENSACIÓN = row[37],
                        COUNTEMPLEADOPEREMPRESA = row[38],
                        COUNTEMPRESAPERREPORT = row[39],
                        COUNTEMPLEADOPERREPORT = row[40],
                        )


def render_to_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path