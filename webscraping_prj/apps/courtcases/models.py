from django.db import models


# Create your models here.
class CaseDetails(models.Model):

    # case details
    case_id = models.AutoField(primary_key=True)
    case_type = models.CharField(max_length=500)
    case_filing_date = models.DateField()
    complainant_name = models.CharField(max_length=500)
    respondent_name = models.CharField(max_length=500)
    registration_rera_number = models.CharField(max_length=100)
    rera_project =  models.CharField(max_length=500)

    # case status
    status_fixed_for =  models.CharField(max_length=500)
    bench_name =  models.CharField(max_length=500)
    court_address = models.TextField()
    pending_for_date_of_decision = models.DateField()

    # additional complainant
    additional_complainant_details = models.TextField()

    class Meta:
        abstract = False
        db_table = "Case_details"
        verbose_name = "Case_Detail"
        verbose_name_plural = "Case_Details"



class HearingRecordDetails(models.Model):

    hearing_record_id = models.AutoField(primary_key=True)
    website_id = models.IntegerField()
    case_number = models.ForeignKey(CaseDetails, on_delete=models.CASCADE)
    bench_name = models.CharField(max_length=200)
    next_hearing_date_fxed = models.DateField()
    purpose_of_hearing = models.TextField()
    date_fixed_for_proceeding = models.DateField()


    class Meta:
        abstract = False
        db_table = "Hearing_record_detasils"
        verbose_name = "Hearing_record_Detail"
        verbose_name_plural = "Hearing_record_Details"




class OrderDetails(models.Model):

    order_record_id = models.AutoField(primary_key=True)
    order_doc_title = models.CharField(max_length=500)
    order_date = models.DateField()
    order_doc = models.FileField()

    class Meta:
        abstract = False
        db_table = "Order_details"
        verbose_name = "Order_Detail"
        verbose_name_plural = "Order_Details"




class CaseTransferDetails(models.Model):

    case_transfer_id = models.AutoField(primary_key=True)
    case_from_bench = models.CharField(max_length=500)
    case_to_bench = models.CharField(max_length=500)
    transfer_number = models.CharField(max_length=300)
    transfer_date = models.DateField()
    transfer_remarks = models.TextField()

    class Meta:
        abstract = False
        db_table = "Case_Transfer_details"
        verbose_name = "Case_Transfer_Detail"
        verbose_name_plural = "Case_Transfer_Details"

