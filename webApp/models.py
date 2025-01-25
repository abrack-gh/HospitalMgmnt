from django.db import models


class Patient(models.Model):

    patient_firstName = models.CharField(max_length=30)
    patient_lastName = models.CharField(max_length=30)
    patient_date_of_birth = models.DateField()
    patient_address_firstLine = models.CharField(max_length=30)
    patient_address_secondLine = models.CharField(max_length=30)
    patient_address_town = models.CharField(max_length=30)
    patient_address_county = models.CharField(max_length=30)
    patient_address_postCode = models.CharField(max_length=30)
    patient_insurance_provider = models.CharField(max_length=30)
    patient_insurance_number = models.CharField(max_length=30)
    system_user_type = models.CharField(max_length=30)


class Consultant(models.Model):

    SPECIALISATION = {
        "Cv": "Cardiovascular",
        "Oc": "Oncology",
        "Ug": "Urology",
        "A": "Anaesthetist"
    }

    consultant_firstName = models.CharField(max_length=30)
    consultant_lastName = models.CharField(max_length=30)
    specialisation = models.CharField(max_length=30, choices=SPECIALISATION)


class Procedure(models.Model):

    PROCEDURE_TYPE = {
        "Cv": "Cardiovascular",
        "Oc": "Oncology",
        "Ug": "Urology",
    }

    PROCEDURE_CODES = {
        "CV01": "Initial Heart Screening",
        "OC01": "Initial Cancer Screening",
        "UG01": "Initial Urology Screening"
    }

    procedure_name = models.CharField(max_length=100)
    procedure_type = models.CharField(max_length=8, choices=PROCEDURE_TYPE)
    procedure_code = models.CharField(max_length=8, choices=PROCEDURE_CODES)
    procedure_date = models.DateField()
    procedure_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='procedures')
    procedure_consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='procedures')
    procedure_anaesthetist = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='procedures')
    procedure_notes = models.TextField(blank=True, null=True)

    def validation_check_consultant(self):

        if self.procedure_code != self.procedure_consultant.specailisation:
            raise ValidationError({
                'consultant': f"The consultant's spetialisation ({self.procedure_consultant.specailisation})"
                              f"does not match the procedure field, ({self.procedure_type})"
            })

    def __str__(self):
        return f"{self.procedure_name} for {self.procedure_patient} on {self.procedure_date}"

