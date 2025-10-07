# from rest_framework import serializers
# from .models import Student, Event, Attendance


# class StudentSerializer(serializers.ModelSerializer):
#     is_present = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Student
#         fields = ['roll_number', 'name', 'email', 'phone', 'department', 'year', 'is_present']
    
#     def get_is_present(self, obj):
#         event_id = self.context.get('event_id')
#         if event_id:
#             return Attendance.objects.filter(
#                 student=obj,
#                 event_id=event_id,
#                 is_present=True
#             ).exists()
#         return False


# class EventSerializer(serializers.ModelSerializer):
#     total_attendees = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Event
#         fields = ['id', 'name', 'description', 'date', 'time', 'venue', 'is_active', 'total_attendees']
    
#     def get_total_attendees(self, obj):
#         return Attendance.objects.filter(event=obj, is_present=True).count()


# class AttendanceSerializer(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     student_department = serializers.CharField(source='student.department', read_only=True)
    
#     class Meta:
#         model = Attendance
#         fields = ['id', 'event', 'student', 'student_name', 'student_department', 'marked_at', 'is_present']
#         read_only_fields = ['marked_at']


# class MarkAttendanceSerializer(serializers.Serializer):
#     roll_number = serializers.CharField(max_length=8)
#     event_id = serializers.IntegerField()
    
#     def validate_roll_number(self, value):
#         if not Student.objects.filter(roll_number=value).exists():
#             raise serializers.ValidationError("Student with this roll number does not exist.")
#         return value
    
#     def validate_event_id(self, value):
#         if not Event.objects.filter(id=value, is_active=True).exists():
#             raise serializers.ValidationError("Event does not exist or is not active.")
#         return value
    
#     def create(self, validated_data):
#         student = Student.objects.get(roll_number=validated_data['roll_number'])
#         event = Event.objects.get(id=validated_data['event_id'])
        
#         attendance, created = Attendance.objects.get_or_create(
#             student=student,
#             event=event,
#             defaults={'is_present': True}
#         )
        
#         if not created and not attendance.is_present:
#             attendance.is_present = True
#             attendance.save()
        
#         return attendance







# serializers.py - UPDATE THIS FILE

from rest_framework import serializers
from .models import Student, Event, Attendance


class StudentSerializer(serializers.ModelSerializer):
    is_present = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['roll_number', 'name', 'email', 'phone', 'department', 'year', 'is_present']
    
    def get_is_present(self, obj):
        event_id = self.context.get('event_id')
        if event_id:
            return Attendance.objects.filter(
                student=obj,
                event_id=event_id,
                is_present=True
            ).exists()
        return False


class EventSerializer(serializers.ModelSerializer):
    total_attendees = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'venue', 'is_active', 'total_attendees']
    
    def get_total_attendees(self, obj):
        return Attendance.objects.filter(event=obj, is_present=True).count()


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_department = serializers.CharField(source='student.department', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'event', 'student', 'student_name', 'student_roll', 'student_department', 'marked_at', 'is_present']
        read_only_fields = ['marked_at']


class MarkAttendanceSerializer(serializers.Serializer):
    # FIXED: Changed max_length from 8 to 20 to support both 8 and 10 digit roll numbers
    roll_number = serializers.CharField(max_length=20)
    event_id = serializers.IntegerField()
    
    def validate_roll_number(self, value):
        # Strip whitespace and validate
        value = value.strip()
        if not Student.objects.filter(roll_number=value).exists():
            raise serializers.ValidationError(f"Student with roll number '{value}' does not exist.")
        return value
    
    def validate_event_id(self, value):
        if not Event.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Event does not exist or is not active.")
        return value
    
    def create(self, validated_data):
        student = Student.objects.get(roll_number=validated_data['roll_number'])
        event = Event.objects.get(id=validated_data['event_id'])
        
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            event=event,
            defaults={'is_present': True}
        )
        
        if not created:
            # If attendance already exists, update the timestamp
            if not attendance.is_present:
                attendance.is_present = True
                attendance.save()
            else:
                # Already marked, but update timestamp
                attendance.save()
        
        return attendance