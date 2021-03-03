from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bookings.models import Store
from django.http import JsonResponse
from bookings.db_setup import insert_one_doc,find_doc,update_doc
from .db_setup import MongoConnection,MyCollection
import uuid


class Bookapp(View):

    dbconnection = None

    @csrf_exempt
    def get(self, request):
        return self.place_request(request)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.db_update(request)



    def place_request(self,request):
        return render(request, "bookings/request_info.html")

    @csrf_exempt
    def db_update(self, request):
        """ 1 - place request """

        patient_name = request.POST.get('patient_name', None)
        doctor_name = request.POST.get('doctor_name', None)
        age = request.POST.get('age', None)
        appointment_time = request.POST.get('appointment_time', None)

        st=Store();
        doc=st.create_request(patient_name,doctor_name,age,appointment_time)
        id=str(uuid.uuid4());
        doc['_id']=id;

        self.dbconnection = MyCollection()

        self.insert(doc,1);

        sts= self.check_avail(doc['doctor_name'])

        if(sts):
            doc2= st.create_appointment(doc,id);
            self.insert(doc2, 2);
            return self.display_appointments()

        else:
            return HttpResponse("<h3>Requested Doctor not Available</h3>")

    def display_appointments(self):
        cnf = self.dbconnection.get_collection("Confirmed_appointments")
        return JsonResponse(find_doc(cnf), safe=False)


    def insert(self, item, i):

        if i == 1:
            app = self.dbconnection.get_collection("Appointment_requests")
            insert_one_doc(app, item)
        elif i == 2:
            bills = self.dbconnection.get_collection("Confirmed_appointments")
            insert_one_doc(bills, item)
        else:
            pass

    def check_avail(self,dname):

        app = self.dbconnection.get_collection("Doctors")
        doctor=find_doc(app,"name",dname)
        if(doctor["availability"]==True):
            update_doc(app,"name",dname);
            return True
        else:
            return False



