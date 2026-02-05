from django.contrib import admin
from .models import (
    DataProcess,
    FacultyCI,
    ProgramCI,
    AssessValidity,
    AccredReport,
    AnnualReport
)

# Register models with custom admin displays

# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('code', 'name')
#     search_fields = ('name', 'code')
#
# @admin.register(Program)
# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code', 'department')
#     list_filter = ('department',)
#     search_fields = ('name', 'code')
#
# class LearningOutcomeInline(admin.TabularInline):
#     model = LearningOutcome
#     extra = 1
#
# class CourseGraduateAttributeInline(admin.TabularInline):
#     model = CourseGraduateAttribute
#     extra = 1
#
# class AssessmentMethodInline(admin.TabularInline):
#     model = AssessmentMethod
#     extra = 1
#
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('code', 'name', 'credits', 'department', 'program', 'accreditation_status', 'updated_at')
#     list_filter = ('department', 'program', 'accreditation_status', 'level')
#     search_fields = ('code', 'name', 'description')
#     inlines = [LearningOutcomeInline, CourseGraduateAttributeInline, AssessmentMethodInline]
#
# @admin.register(LearningOutcome)
# class LearningOutcomeAdmin(admin.ModelAdmin):
#     list_display = ('course', 'order', 'description')
#     list_filter = ('course__department',)
#     search_fields = ('description', 'course__code', 'course__name')
#
# @admin.register(GraduateAttribute)
# class GraduateAttributeAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name', 'description')
#
# @admin.register(CourseGraduateAttribute)
# class CourseGraduateAttributeAdmin(admin.ModelAdmin):
#     list_display = ('course', 'attribute', 'level')
#     list_filter = ('attribute', 'level')
#     search_fields = ('course__code', 'course__name', 'attribute__name')
#
# @admin.register(AssessmentMethod)
# class AssessmentMethodAdmin(admin.ModelAdmin):
#     list_display = ('course', 'name', 'weight')
#     list_filter = ('course__department',)
#     search_fields = ('name', 'course__code', 'course__name')
#
# @admin.register(AssessmentOutcomeMapping)
# class AssessmentOutcomeMappingAdmin(admin.ModelAdmin):
#     list_display = ('assessment', 'outcome')
#     list_filter = ('assessment__course',)
#
# @admin.register(CSVUpload)
# class CSVUploadAdmin(admin.ModelAdmin):
#     list_display = ('file_name', 'file_type', 'user', 'upload_date', 'status')
#     list_filter = ('file_type', 'status', 'upload_date')
#     search_fields = ('file_name', 'user__username')
#     readonly_fields = ('upload_date',)
#
# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role', 'department')
#     list_filter = ('role', 'department')
#     search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
