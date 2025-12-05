from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Falta, Excusa
from .serializers import FaltaSerializer, ExcusaSerializer

import datetime

def dashboard(request):
    total_faltas = Falta.objects.count()
    tardanzas = Falta.objects.filter(es_tardanza=True).count()
    sin_excusa = Falta.objects.filter(fecha_limite_excusa__isnull=True).count()

    context = {
        'total_faltas': total_faltas,
        'tardanzas': tardanzas,
        'sin_excusa': sin_excusa,
        'faltas': Falta.objects.all()
    }
    return render(request, 'dashboard.html', context)


class FaltaViewSet(viewsets.ModelViewSet):
    queryset = Falta.objects.all()
    serializer_class = FaltaSerializer

    def add_business_days(self, start_date, days):
        current = start_date
        added = 0
        while added < days:
            current += datetime.timedelta(days=1)
            if current.weekday() < 5:
                added += 1
        return current

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        fecha_falta = data.get('fecha_falta')
        aprendiz_id = data.get('aprendiz')
        es_tardanza_str = data.get('es_tardanza', 'false').lower()
        es_tardanza = es_tardanza_str in ['true', '1', 'yes']
        
        # Validar que la fecha no sea en el futuro
        if fecha_falta:
            try:
                fecha_falta_dt = datetime.datetime.strptime(fecha_falta, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # VALIDACIÓN CLAVE: Rechazar fechas en el futuro
            hoy = datetime.datetime.now().date()
            if fecha_falta_dt > hoy:
                return Response(
                    {'error': f'No se puede registrar una falta en una fecha futura. Fecha ingresada: {fecha_falta_dt}, Hoy: {hoy}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Contar faltas existentes (no tardanzas)
            faltas_count = Falta.objects.filter(aprendiz_id=aprendiz_id, es_tardanza=False).count()
            if not es_tardanza and faltas_count >= 3:
                return Response(
                    {'error': 'El aprendiz ya tiene el máximo de 3 faltas permitidas.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Contar ausencias existentes (tardanzas)
            ausencias_count = Falta.objects.filter(aprendiz_id=aprendiz_id, es_tardanza=True).count()
            if es_tardanza and ausencias_count >= 3:
                return Response(
                    {'error': 'El aprendiz ya tiene el máximo de 3 ausencias permitidas.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calcular fecha límite de excusa
            fecha_limite = self.add_business_days(fecha_falta_dt, 3)
            data['fecha_limite_excusa'] = fecha_limite
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ExcusaViewSet(viewsets.ModelViewSet):
    queryset = Excusa.objects.all()
    serializer_class = ExcusaSerializer

    def get_queryset(self):
        # Filtrar excusas solo del usuario autenticado (aprendiz)
        user = self.request.user
        if user.is_authenticated:
            return Excusa.objects.filter(falta__aprendiz=user)
        return Excusa.objects.none()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        falta_id = data.get('falta')
        motivo = data.get('motivo')
        documento_adjunto = request.FILES.get('documento_adjunto')
        
        try:
            falta = Falta.objects.get(pk=falta_id)
        except Falta.DoesNotExist:
            return Response(
                {'error': 'Falta no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validar que la falta pertenezca al usuario autenticado
        if falta.aprendiz != request.user:
            return Response(
                {'error': 'No tienes permiso para cargar excusa de otra persona'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        fecha_presentacion = datetime.datetime.now().date()
        estado = 'P'
        
        # Validar si la excusa está vencida
        if fecha_presentacion > falta.fecha_limite_excusa:
            estado = 'V'
            return Response(
                {'error': 'El plazo para cargar la excusa ha vencido', 'estado': 'V'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que no exista una excusa previa para esta falta
        if Excusa.objects.filter(falta=falta).exists():
            return Response(
                {'error': 'Esta falta ya tiene una excusa registrada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        excusa = Excusa.objects.create(
            falta=falta,
            motivo=motivo,
            documento_adjunto=documento_adjunto,
            estado=estado
        )
        serializer = self.get_serializer(excusa)
        return Response(serializer.data, status=status.HTTP_201_CREATED)