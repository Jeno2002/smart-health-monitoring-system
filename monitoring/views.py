from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HealthRecord, Notification
from .forms import HealthRecordForm
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from django.http import JsonResponse
from .models import HealthRecord, PatientProfile
from .forms import PatientForm
from django.utils.timezone import now
from .models import Notification
from .models import Patient
from .models import HealthData  
from django.contrib.auth import logout
import monitoring.models as models
models.HealthRecord
models.Notification
models.Patient.objects.all()
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from .models import HealthCheckupCount
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return render(request,'home.html')

@csrf_exempt
def dashboard(request):
    count = HealthCheckupCount.objects.get(id=1)
    context = {
        'count': count.count,
        'total_count':count.count + 23
    }
    return render(request,'dashboard.html', context)

def login(request):
    return render(request,'login.html')




def register(request):
    return render(request,'register.html')

def analyze_health_data(patient):
    latest_record = HealthRecord.objects.filter(patient=patient).latest('recorded_at')
    message = None

    if latest_record.blood_sugar > 140:
        message = "Your blood sugar is high! Please consult a doctor."
    elif latest_record.blood_pressure != "120/80":
        message = "Your blood pressure is abnormal. Please check with a physician."
    elif latest_record.heart_rate < 60 or latest_record.heart_rate > 100:
        message = "Your heartbeat rate is abnormal. Immediate consultation is advised."

    if message:
        Notification.objects.create(patient=patient, message=message)
        send_notification_email(patient.user.email, message)
        send_sms_notification(patient.contact_number, message)

# Function to send Email notifications
def send_notification_email(email, message):
    send_mail(
        'Health Alert Notification',
        message,
        'noreply@healthsystem.com',
        [email],
        fail_silently=False,
    )


@login_required
def submit_health_data(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        blood_pressure = int(request.POST.get("blood_pressure", 0))
        heart_rate = int(request.POST.get("heart_rate", 0))

        # Save health data
        health_data = HealthData.objects.create(
            patient_id=patient_id,
            blood_pressure=blood_pressure,
            heart_rate=heart_rate,
            timestamp=now()
        )

        # Check if vitals are abnormal
        abnormal = False
        alert_message = ""

        if blood_pressure > 140 or heart_rate > 100:  # Example threshold
            abnormal = True
            alert_message = f"🚨 ALERT: Patient {patient_id} has abnormal vitals!"

            # Save notification in database
            Notification.objects.create(
                message=alert_message,
                is_read=False,
                timestamp=now()
            )

        return JsonResponse({"abnormal": abnormal, "message": alert_message})


def patient_form(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            # Process the data (e.g., save it to the database)
            patient_data = form.cleaned_data
            print(patient_data)  # For testing, replace with saving to DB
            return render(request, "success.html")  # Redirect to success page
    else:
        form = PatientForm()
    
    return render(request, "patient_form.html", {"form": form})

def success(request):
    return render(request, 'success.html') 



# Twilio credentials (Replace with actual values)
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

# Function to send SMS
def send_sms(phone_number, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )


@login_required
def notification(request):
    context = {
        "username": request.user.username,  # Ensure username is passed
        "health_status": get_health_status(request.user),  # Replace with actual function
    }
    return render(request, "notification.html", context)


def send_sms_notification():
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body="Your health alert notification!",
        from_=settings.TWILIO_PHONE_NUMBER,  # Twilio phone number
        to="+11234567890"  # Replace with the recipient's phone number
    )

    return message.sid


def get_latest_notifications(request):
    notifications = Notification.objects.filter(is_read=False).values()
    return JsonResponse(list(notifications), safe=False)

def health_notification(request):
    patient = Patient.objects.filter(created_at__gte="2024-01-01").latest("created_at")
     # Fetch the latest patient record

    context = {
        'name': patient.name,
        'pulse': patient.pulse,
        'heart_rate': patient.heart_rate,
        'blood_pressure': patient.blood_pressure,
    }
    return render(request, 'health_notification.html', context)

def health_result(request):
    return render(request, 'health_result.html') 

def send_alert():
    print("⚠️ Alert! A patient's condition is Critical!") 

def health_monitoring(request):
    return render(request, "health_monitoring.html")  # Load the page

def get_health_data(request, user_id):
    try:
        patient = Patient.objects.get(id=user_id)
        data = {
            "pulse_rate": patient.pulse_rate,
            "heart_rate": patient.heart_rate,
            "blood_pressure": patient.blood_pressure,
            "sugar_level": patient.sugar_level,
        }
        return JsonResponse(data)
    except Patient.DoesNotExist:
        return JsonResponse({"error": "Patient not found"}, status=404)
    

def health_notification(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)  # ✅ Get patient by ID
    except Patient.DoesNotExist:
        patient = None  # ✅ Handle missing patient

    if patient and patient.condition == "Critical":
        send_alert()

    return render(request, "health_notification.html", {"patient": patient})





class CheckUpCount(APIView):
    def post(self, request):
        try:
            count = HealthCheckupCount.objects.get(id=1)
            count.count += 1
            count.save()

        except HealthCheckupCount.DoesNotExist:
            count = HealthCheckupCount.objects.create(id=1, count=1)

        return Response({"count": count.count}, status=status.HTTP_200_OK)

    




# ************************************     LOGIN APIS     ************************

from django.contrib.auth import authenticate 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
import json
from django.contrib.auth.hashers import make_password

class LoginAPIView(APIView):
    def post(self, request):
        try:
            data = request.data  # DRF handles JSON parsing
            email = data.get("email")
            password = data.get("password")

            # Authenticate user
            user = authenticate(username=email, password=password)

            if user is not None:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "Login successful",
                    "status": "success",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)

            return Response({"message": "Invalid credentials", "status": "error"}, status=status.HTTP_401_UNAUTHORIZED)

        except json.JSONDecodeError:
            return Response({"message": "Invalid JSON format", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    def post(self, request):
        """Registers a new user with email, first name, last name, and password."""
        data = request.data
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        # Check if the email is already registered
        if User.objects.filter(username=email).exists():
            return Response({"message": "Email already in use", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)  # Hash the password
        )

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "User registered successfully",
            "status": "success",
            "access_token": access_token,
            "refresh_token": str(refresh)
        }, status=status.HTTP_201_CREATED)
    
class HealthMonitoringAPIView(APIView):
    def post(self, request):
        """API to check patient's health condition."""
        data = request.data  # Get JSON data from request
        
        pulse_rate = data.get("pulse_rate")
        heart_rate = data.get("heart_rate")
        blood_pressure = data.get("blood_pressure")
        sugar_level = data.get("sugar_level")

        # Check if any value is missing
        if pulse_rate is None or heart_rate is None or blood_pressure is None or sugar_level is None:
            return Response({"status": "error", "message": "Please enter all health details."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Define normal ranges
        normal_ranges = {
            "pulse_rate": (60, 100),
            "heart_rate": (60, 100),
            "blood_pressure": (90, 120),  # Systolic range
            "sugar_level": (70, 140)  # Fasting sugar level range
        }

        alerts = []  # Store abnormal conditions
        
        # Check pulse rate
        if not normal_ranges["pulse_rate"][0] <= pulse_rate <= normal_ranges["pulse_rate"][1]:
            alerts.append(f"⚠️ Pulse rate abnormal: {pulse_rate} bpm")
        
        # Check heart rate
        if not normal_ranges["heart_rate"][0] <= heart_rate <= normal_ranges["heart_rate"][1]:
            alerts.append(f"⚠️ Heart rate abnormal: {heart_rate} bpm")
        
        # Check blood pressure
        if not normal_ranges["blood_pressure"][0] <= blood_pressure <= normal_ranges["blood_pressure"][1]:
            alerts.append(f"⚠️ Blood pressure abnormal: {blood_pressure} mmHg")
        
        # Check sugar level
        if not normal_ranges["sugar_level"][0] <= sugar_level <= normal_ranges["sugar_level"][1]:
            alerts.append(f"⚠️ Sugar level abnormal: {sugar_level} mg/dL")

        # Return health condition
        if alerts:
            return Response({"status": "alert", "message": " ".join(alerts)}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "good", "message": "✅ Health condition is good."}, status=status.HTTP_200_OK)
        


# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure user is authenticated

#     def post(self, request):
#         logout(request)
#         return Response({"message": "Successfully logged out."}, status=200)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=200)

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=200)

   