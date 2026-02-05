from accreditation.models import *
from django.db import connection

DataProcess.objects.all().delete()
ProgramCI.objects.all().delete()
FacultyCI.objects.all().delete()
AssessValidity.objects.all().delete()
AccredReport.objects.all().delete()
AnnualReport.objects.all().delete()

with connection.cursor() as cursor:
    cursor.execute("ALTER SEQUENCE accreditation_dataprocess_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE accreditation_programci_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE accreditation_facultyci_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE accreditation_assessvalidity_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE accreditation_accredreport_id_seq RESTART WITH 1;")
    cursor.execute("ALTER SEQUENCE accreditation_annualreport_id_seq RESTART WITH 1;")

print("Database has been wiped, and ids (primary keys for every entry) have been reset")