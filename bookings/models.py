from django.db import models

# Create your models here.

class Store():
    def create_request(self,patient_name,doctor_name,age,appointment_time):
        orderx={};
        orderx['patient_name']=patient_name;
        orderx['doctor_name'] = doctor_name;
        orderx['age'] = age;
        orderx['appointment_time'] = appointment_time;
        return orderx;

    def create_appointment(self, orderx, id):
        billx = {}
        billx['_id'] = id
        billx["Request_details"] = orderx
        billx["Appointment status"]="confirmed"
        return billx