from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Model to store patient details
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's User model
    age = models.IntegerField()
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


# Model to store notifications for health alerts
class Notification(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)  # Link to patient profile
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Stores timestamp automatically
    is_read = models.BooleanField(default=False)  # Default is unread

    def __str__(self):
        return f"Notification for {self.patient.user.username}"


# Patient Model
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    blood_pressure = models.CharField(max_length=10, default="120/80")  # Default value
    heart_rate = models.IntegerField(default=72)
    pulse_rate = models.IntegerField(default=72)  # e.g., "120/80"
    condition = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name



# Health Data Model (Fixed ForeignKey Reference)
class HealthData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # ✅ Corrected reference
    blood_pressure = models.CharField(max_length=10)
    heart_rate = models.IntegerField()
    pulse_rate = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def evaluate_condition(self):
        """Determine the patient's health condition"""
        if (self.pulse_rate < 60 or self.pulse_rate > 100) or (self.heart_rate < 50 or self.heart_rate > 120) \
           or ("180" in self.blood_pressure or "40" in self.blood_pressure) or (self.sugar_level < 70 or self.sugar_level > 180):
            return "Critical"
        elif (60 <= self.pulse_rate <= 100) and (50 <= self.heart_rate <= 100) and ("120" in self.blood_pressure or "80" in self.blood_pressure) \
             and (70 <= self.sugar_level <= 140):
            return "Normal"
        else:
            return "Moderate"
    

    def __str__(self):
        return f"{self.patient.name} - {self.recorded_at}"


# Health Record Model
class HealthRecord(models.Model):
    patient_name = models.CharField(max_length=100)
    pulse = models.IntegerField()
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.patient_name


class HealthCheckupCount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.count)