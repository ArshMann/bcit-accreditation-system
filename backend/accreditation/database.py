"""
This module houses the classes and methods to interact with the database.
"""

from .models import (
    DataProcess,
    FacultyCI,
    ProgramCI,
    AssessValidity,
    AccredReport,
    AnnualReport,
    Faculty
)
from .utils import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal

def upload_data(program: str,
                course: str,
                term: str,
                prog_term: int,
                instr_first_name: str,
                instr_last_name: str,
                ga: str,
                gai: str,
                instr_level: str,
                alignment: str,
                clos: str,
                assess_type: str,
                assess_weight: float,
                assess_max: int,
                total_score: float,
                question_max: int,
                gai_score: float,
                assess_title: str,
                assess_descript: str,
                quest_text: str,
                student_id: str,
                instr_comments: str):
    try:
        cohort = get_cohort(prog_term, term, program)
        achievement_level = Decimal(str(round(get_achievement_level(gai_score, question_max), 2)))


        dp_result = DataProcessDAO.insert(term=term, 
                                          program=program, 
                                          course=course, 
                                          gai=gai)
        
        if isinstance(dp_result, dict) and not dp_result.get("success", True):
            print("DataProcess insert failed:", dp_result["errors"])

        fc_result = FacultyCIDAO.insert(course=course, 
                                        term=term, 
                                        instr_first_name=encrypt(instr_first_name),
                                        instr_last_name=encrypt(instr_last_name), 
                                        assess_title=assess_title,
                                        gai_score=encrypt(gai_score), 
                                        total_score=total_score, 
                                        cohort=cohort)
        
        if isinstance(fc_result, dict) and not fc_result.get("success", True):
            print("FacultyCI insert failed:", fc_result["errors"])

        pc_result = ProgramCIDAO.insert(term=term, 
                                        ga=ga, 
                                        gai=gai, 
                                        prog_term=prog_term, 
                                        gai_score=encrypt(gai_score), 
                                        total_score=total_score,
                                        achievement_level=achievement_level, 
                                        cohort=cohort)
        
        if isinstance(pc_result, dict) and not pc_result.get("success", True):
            print("ProgramCI insert failed:", pc_result["errors"])

        av_result = AssessValidityDAO.insert(gai=gai, 
                                             ga=ga, 
                                             course=course, 
                                             question_max=question_max,
                                             alignment=alignment, 
                                             gai_score=encrypt(gai_score), 
                                             total_score=total_score,
                                             assess_max=assess_max, 
                                             assess_weight=assess_weight,
                                             assess_descript=assess_descript, 
                                             clos=clos)
        
        if isinstance(av_result, dict) and not av_result.get("success", True):
            print("AssessValidity insert failed:", av_result["errors"])

        ar_result = AccredReportDAO.insert(program=program, 
                                           term=term, 
                                           ga=ga, 
                                           gai=gai, 
                                           assess_type=assess_type,
                                           quest_text=quest_text, 
                                           alignment=alignment, 
                                           instr_level=instr_level,
                                           achievement_level=achievement_level, 
                                           student_id=encrypt(student_id))
        
        if isinstance(ar_result, dict) and not ar_result.get("success", True):
            print("AccredReport insert failed:", ar_result["errors"])

        anr_result = AnnualReportDAO.insert(program=program, 
                                            term=term, 
                                            course=course, 
                                            ga=ga, 
                                            gai=gai,
                                            student_id=encrypt(student_id), 
                                            achievement_level=achievement_level,
                                            assess_type=assess_type, 
                                            instr_comments=instr_comments)
        
        if isinstance(anr_result, dict) and not anr_result.get("success", True):
            print("AnnualReport insert failed:", anr_result["errors"])

    except Exception as e:
        print("Unexpected error in upload_data():", str(e))

def get_flattened_data_for_export():
    ids = DataProcess.objects.values_list('id', flat=True).order_by('-id')
    results = []

    for id in ids:
        try:
            dp = DataProcess.objects.get(id=id)
            fc = FacultyCI.objects.get(id=id)
            pc = ProgramCI.objects.get(id=id)
            av = AssessValidity.objects.get(id=id)
            ar = AccredReport.objects.get(id=id)
            anr = AnnualReport.objects.get(id=id)

            row = {
                "id": id,
                "term": dp.term,
                "cohort": pc.cohort,
                "program": dp.program,
                "prog_term": pc.prog_term,
                "course": dp.course,
                "instr_first_name": decrypt(fc.instr_first_name, str),
                "instr_last_name": decrypt(fc.instr_last_name, str),
                "student_id": decrypt(ar.student_id, str),
                "ga": ar.ga,
                "gai": ar.gai,
                "achievement_level": pc.achievement_level,
                "instr_level": ar.instr_level,
                "assess_title": fc.assess_title,
                "assess_type": ar.assess_type,
                "assess_descript": av.assess_descript,
                "assess_weight": av.assess_weight,
                "assess_max": av.assess_max,
                "alignment": av.alignment,
                "clos": av.clos,
                "total_score": fc.total_score,
                "gai_score": decrypt(fc.gai_score, Decimal),
                "quest_text": ar.quest_text,
                "question_max": av.question_max,
                "instr_comments": anr.instr_comments,
                "created_at": dp.created_at
            }

            results.append(row)
        except Exception:
            #
            continue

    return results

def delete_entry(id):
    """
    Delete the entry with id matching from each of the db tables

    :return: False if any issues, True is successfully deleted
    """
    if DataProcessDAO.delete(id) == False:
        return False
    if FacultyCIDAO.delete(id) == False:
        return False
    if ProgramCIDAO.delete(id) == False:
        return False
    if AssessValidityDAO.delete(id) == False:
        return False
    if AccredReportDAO.delete(id) == False:
        return False
    if AnnualReportDAO.delete(id) == False:
        return False
    return True

def delete_user(id):
    """
    Delete user from the database matching with id
    """
    try:
        user = User.objects.get(id=id)

        # Try to delete related Faculty if it exists
        try:
            faculty = Faculty.objects.get(user=user)
            faculty.delete()
        except Faculty.DoesNotExist:
            pass  # Faculty is optional, skip if not found

        user.delete()
        return True

    except User.DoesNotExist:
        print(f"User with id {id} does not exist.")
        return False
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False



class DataProcessDAO:
    @staticmethod
    def insert(**data):
        try:
            instance = DataProcess(**data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        except Exception as e:
            return {"success": False, "errors": str(e)}
        
    @staticmethod
    def get_all():
        return DataProcess.objects.all()
    
    @staticmethod
    def filter_by(**kwargs):
        return DataProcess.objects.filter(**kwargs) 
    
    @staticmethod
    def update(pk, **kwargs):
        try:
            obj = DataProcess.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.full_clean()
            obj.save()
            return obj
        except DataProcess.DoesNotExist:
            return None
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        
    @staticmethod
    def delete(pk):
        try:
            obj = DataProcess.objects.get(id=pk)
            obj.delete()
            return True
        except DataProcess.DoesNotExist:
            return False

class FacultyCIDAO:
    @staticmethod
    def insert(**data):
        try:
            instance = FacultyCI(**data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        except Exception as e:
            return {"success": False, "errors": str(e)}
        
    @staticmethod
    def get_all():
        return FacultyCI.objects.all()
    
    @staticmethod
    def filter_by(**kwargs):
        return FacultyCI.objects.filter(**kwargs) 
    
    @staticmethod
    def update(pk, **kwargs):
        try:
            obj = FacultyCI.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.full_clean()
            obj.save()
            return obj
        except FacultyCI.DoesNotExist:
            return None
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}

    @staticmethod
    def delete(pk):
        try:
            obj = FacultyCI.objects.get(pk=pk)
            obj.delete()
            return True
        except FacultyCI.DoesNotExist:
            return False
        
class ProgramCIDAO:
    @staticmethod
    def insert(**data):
        try:
            instance = ProgramCI(**data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        except Exception as e:
            return {"success": False, "errors": str(e)}
        
    @staticmethod
    def get_all():
        return ProgramCI.objects.all()
    
    @staticmethod
    def filter_by(**kwargs):
        return ProgramCI.objects.filter(**kwargs) 
    
    @staticmethod
    def update(pk, **kwargs):
        try:
            obj = ProgramCI.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.full_clean()
            obj.save()
            return obj
        except ProgramCI.DoesNotExist:
            return None
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
    
    @staticmethod
    def delete(pk):
        try:
            obj = ProgramCI.objects.get(pk=pk)
            obj.delete()
            return True
        except ProgramCI.DoesNotExist:
            return False

class AssessValidityDAO:
    @staticmethod
    def insert(**data):
        try:
            instance = AssessValidity(**data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        except Exception as e:
            return {"success": False, "errors": str(e)}
        
    @staticmethod
    def get_all():
        return AssessValidity.objects.all()
    
    @staticmethod
    def filter_by(**kwargs):
        return AssessValidity.objects.filter(**kwargs) 
    
    @staticmethod
    def update(pk, **kwargs):
        try:
            obj = AssessValidity.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.full_clean()
            obj.save()
            return obj
        except AssessValidity.DoesNotExist:
            return None
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        
    @staticmethod
    def delete(pk):
        try:
            obj = AssessValidity.objects.get(pk=pk)
            obj.delete()
            return True
        except AssessValidity.DoesNotExist:
            return False
    
class AccredReportDAO:
    @staticmethod
    def insert(**data):
        try:
            instance = AccredReport(**data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        except Exception as e:
            return {"success": False, "errors": str(e)}
        
    @staticmethod
    def get_all():
        return AccredReport.objects.all()
    
    @staticmethod
    def filter_by(**kwargs):
        return AccredReport.objects.filter(**kwargs) 
    
    @staticmethod
    def update(pk, **kwargs):
        try:
            obj = AccredReport.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.full_clean()
            obj.save()
            return obj
        except AccredReport.DoesNotExist:
            return None
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
    
    @staticmethod
    def delete(pk):
        try:
            obj = AccredReport.objects.get(pk=pk)
            obj.delete()
            return True
        except AccredReport.DoesNotExist:
            return False

class AnnualReportDAO:
    @staticmethod
    def insert(**data):
        try:
            instance = AnnualReport(**data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
        except Exception as e:
            return {"success": False, "errors": str(e)}
        
    @staticmethod
    def get_all():
        return AnnualReport.objects.all()
    
    @staticmethod
    def filter_by(**kwargs):
        return AnnualReport.objects.filter(**kwargs) 
    
    @staticmethod
    def update(pk, **kwargs):
        try:
            obj = AnnualReport.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.full_clean()
            obj.save()
            return obj
        except AnnualReport.DoesNotExist:
            return None
        except ValidationError as e:
            return {"success": False, "errors": e.message_dict}
    
    @staticmethod
    def delete(pk):
        try:
            obj = AnnualReport.objects.get(pk=pk)
            obj.delete()
            return True
        except AnnualReport.DoesNotExist:
            return False
