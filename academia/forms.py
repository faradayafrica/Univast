from django import forms
from .models import AcademicCalendar, AcademicSession, Semester

class AcademicCalendarForm(forms.ModelForm):
    class Meta:
        model = AcademicCalendar
        fields = '__all__'
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # For creating a new instance, don't restrict academic_session queryset initially
    #     self.fields['academic_session'].queryset = AcademicSession.objects.none()
        
    #     # # Limit the semester queryset to the selected academic_session
    #     # academic_session = self.cleaned_data.get('academic_session')
    #     # if academic_session:
    #     self.fields['semester'].queryset = Semester.objects.filter(academic_session=academic_session)
    #     # else:
    #     #     self.fields['semester'].queryset = Semester.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        school = cleaned_data.get('school')
        academic_session = cleaned_data.get('academic_session')
        semester = cleaned_data.get('semester')

        if academic_session and semester:
            if academic_session.school != school:
                raise forms.ValidationError("The selected academic session must belong to the same school.")
            
            if semester.academic_session != academic_session:
                raise forms.ValidationError("The selected semester must belong to the same academic session.")

        return cleaned_data