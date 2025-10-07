from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Student, Event, Attendance
from .serializers import (
    StudentSerializer, EventSerializer, 
    AttendanceSerializer, MarkAttendanceSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=False, methods=['get'])
    def by_event(self, request):
        event_id = request.query_params.get('event_id')
        if not event_id:
            return Response(
                {'error': 'event_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        students = Student.objects.all()
        serializer = self.get_serializer(
            students, 
            many=True, 
            context={'event_id': event_id}
        )
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        event = self.get_object()
        total_students = Student.objects.count()
        present_count = Attendance.objects.filter(
            event=event, 
            is_present=True
        ).count()
        absent_count = total_students - present_count
        
        return Response({
            'event_name': event.name,
            'total_students': total_students,
            'present': present_count,
            'absent': absent_count,
            'attendance_percentage': round((present_count / total_students * 100), 2) if total_students > 0 else 0
        })
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_events = Event.objects.filter(is_active=True)
        serializer = self.get_serializer(active_events, many=True)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    @action(detail=False, methods=['post'])
    def mark(self, request):
        serializer = MarkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            attendance = serializer.save()
            response_serializer = AttendanceSerializer(attendance)
            return Response({
                'message': 'Attendance marked successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_event(self, request):
        event_id = request.query_params.get('event_id')
        if not event_id:
            return Response(
                {'error': 'event_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendances = Attendance.objects.filter(
            event_id=event_id, 
            is_present=True
        ).select_related('student')
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)