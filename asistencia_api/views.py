from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Falta, Excusa
from .serializers import FaltaSerializer, ExcusaSerializer

import datetime

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
        if fecha_falta:
            fecha_falta_dt = datetime.datetime.strptime(fecha_falta, '%Y-%m-%d').date()
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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        falta_id = data.get('falta')
        motivo = data.get('motivo')
        documento_adjunto = request.FILES.get('documento_adjunto')
        falta = Falta.objects.get(pk=falta_id)
        fecha_presentacion = datetime.datetime.now().date()
        estado = 'P'
        if fecha_presentacion > falta.fecha_limite_excusa:
            estado = 'V'
        excusa = Excusa.objects.create(
            falta=falta,
            motivo=motivo,
            documento_adjunto=documento_adjunto,
            estado=estado
        )
        serializer = self.get_serializer(excusa)
        return Response(serializer.data, status=status.HTTP_201_CREATED)