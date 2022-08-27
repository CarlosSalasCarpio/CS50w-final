from pyexpat import model
from django.db import models

# Create your models here.
class Employees(models.Model):
    EMPRESA = models.CharField(max_length=64)
    EMPLEADO = models.CharField(max_length=64)
    FECHARETIRO = models.CharField(max_length=64)
    TOTALSUELDO = models.CharField(max_length=64)
    OTROS = models.CharField(max_length=64)
    CODCC = models.CharField(max_length=64)
    NOMCC = models.CharField(max_length=64)
    SEXO = models.CharField(max_length=64)
    TIPODOCUMENTO = models.CharField(max_length=64)
    NÚMERODEIDENTIFICACIÓN = models.CharField(max_length=64)
    CIUDADDOCUMENTO = models.CharField(max_length=64)
    FECHADENACIMIENTO = models.CharField(max_length=64)
    CIUDADDENACIMIENTO = models.CharField(max_length=64)
    FECHADEINGRESO = models.CharField(max_length=64)
    CÓDIGOEMPLEDO = models.CharField(max_length=64)
    NOMBREDELCARGO = models.CharField(max_length=64)
    MOTIVODELCARGO = models.CharField(max_length=64)
    NOMBREESTRUCTURACARGO = models.CharField(max_length=64)
    DESCRIPCIÓNDELMOTIVO = models.CharField(max_length=64)
    VALORSUELDO = models.CharField(max_length=64)
    MOTIVOCONTRATO = models.CharField(max_length=64)
    TIPODECONTRATO = models.CharField(max_length=64)
    NOMBRETIPOTRABAJADOR = models.CharField(max_length=64)
    NOMBRETIPOSALARIO = models.CharField(max_length=64)
    NOMBRENORMALABORAL = models.CharField(max_length=64)
    NOMBRELEGISLACIÓNLABORAL = models.CharField(max_length=64)
    UBICACIÓNGEOGRÁFICA = models.CharField(max_length=64)
    NOMBREJORNADA = models.CharField(max_length=64)
    NOMBREFORMADEPAGO = models.CharField(max_length=64)
    CUENTADEPAGO = models.CharField(max_length=64)
    TIPOCUENTA = models.CharField(max_length=64)
    SUCURSALDEPAGO = models.CharField(max_length=64)
    METODODEPAGO = models.CharField(max_length=64)
    EPS = models.CharField(max_length=64)
    FONDOSDEPENSIONES = models.CharField(max_length=64)
    FONDODECESANTÍAS = models.CharField(max_length=64)
    RIESGOSPROFESIONALES = models.CharField(max_length=64)
    CAJADECOMPENSACIÓN = models.CharField(max_length=64)
    COUNTEMPLEADOPEREMPRESA = models.CharField(max_length=64)
    COUNTEMPRESAPERREPORT = models.CharField(max_length=64)
    COUNTEMPLEADOPERREPORT = models.CharField(max_length=64)

class Desprendibles(models.Model):
    fortnight = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='media/')

    #def __str__(self):
        #return self.title
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)
