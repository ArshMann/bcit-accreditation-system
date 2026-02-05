from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


GAI_CHOICES = [
    ('1.1', '1.1'), ('1.2', '1.2'), ('1.3', '1.3'), ('1.4', '1.4'),
    ('2.1', '2.1'), ('2.2', '2.2'), ('2.3', '2.3'),
    ('3.1', '3.1'), ('3.2', '3.2'), ('3.3', '3.3'), ('3.4', '3.4'),
    ('4.1', '4.1'), ('4.2', '4.2'), ('4.3', '4.3'), ('4.4', '4.4'),
    ('5.1', '5.1'), ('5.2', '5.2'), ('5.3', '5.3'), ('5.4', '5.4'),
    ('6.1', '6.1'), ('6.2', '6.2'), ('6.3', '6.3'), ('6.4', '6.4'), ('6.5', '6.5'),
    ('7.1', '7.1'), ('7.2', '7.2'), ('7.3', '7.3'), ('7.4', '7.4'),
    ('8.1', '8.1'), ('8.2', '8.2'), ('8.3', '8.3'),
    ('9.1', '9.1'), ('9.2', '9.2'), ('9.3', '9.3'), ('9.4', '9.4'),
    ('10.1', '10.1'), ('10.2', '10.2'), ('10.3', '10.3'),
    ('11.1', '11.1'), ('11.2', '11.2'), ('11.3', '11.3'),
    ('12.1', '12.1'), ('12.2', '12.2'), ('12.3', '12.3'), ('12.4', '12.4')
]
ASSESSMENT_TYPE_CHOICES = [
    ('Assignment', 'Assignment'),
    ('Project', 'Project'),
    ('Lab report', 'Lab report'),
    ('Presentation', 'Presentation'),
    ('Peer-Assessment', 'Peer-Assessment'),
    ('Final exam', 'Final exam'),
    ('Mid-term', 'Mid-term'),
    ('Quiz', 'Quiz'),
    ('Homework', 'Homework'),
    ('Self-Assessment', 'Self-Assessment'),
    ('Other', 'Other'),
]
ALIGNMENT_CHOICES = [("Perfectly", "Perfectly"),
                     ("Highly", "Highly"),
                     ("Mostly", "Mostly"),
                     ("Somewhat", "Somewhat")
]
PROGRAM_CHOICES = [('ELEX', 'ELEX'), ('CIVL', 'CIVL'), ('MECH', 'MECH'),('MINE', 'MINE')]


class DataProcess(models.Model):
    term = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    program = models.CharField(max_length=4, choices=PROGRAM_CHOICES)

    course = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    gai = models.CharField(
        max_length=4,
        choices=GAI_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Term: {self.term} | Program: {self.program} | Course: {self.course} | GAI: {self.gai}"


class FacultyCI(models.Model):
    course = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    term = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    instr_first_name = models.CharField(max_length=250)
    instr_last_name = models.CharField(max_length=250)
    assess_title = models.CharField(max_length=12)
    gai_score = models.CharField(max_length=250)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(999.99)])
    cohort = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Course: {self.course} | Term: {self.term} | Instructor First Name: {self.instr_first_name} | "
                f"Instructor Last Name: {self.instr_last_name} | Assessment Title: {self.assess_title} | "
                f"Total Score: {self.total_score} | Cohort: {self.cohort} | GAI Score: {self.gai_score}")


class ProgramCI(models.Model):
    term = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    ga = models.CharField(
        max_length=4,
        choices=[(f'GA{i}', f'GA{i}') for i in range(1, 13)]
    )
    gai = models.CharField(
        max_length=4,
        choices=GAI_CHOICES
    )
    gai_score = models.CharField(max_length=250)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(999.99)])
    achievement_level = models.DecimalField(max_digits=5, decimal_places=2)
    cohort = models.CharField(max_length=11)
    prog_term = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Term: {self.term} | GA: {self.ga} | GAI: {self.gai} | Total Score: "
                f"{self.total_score} | Achievement Level: {self.achievement_level} | Cohort: {self.cohort} | "
                f"GAI Score: {self.gai_score}")


class AssessValidity(models.Model):
    gai = models.CharField(
        max_length=4,
        choices=GAI_CHOICES
    )
    ga = models.CharField(
        max_length=4,
        choices=[(f'GA{i}', f'GA{i}') for i in range(1, 13)]
    )
    course = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    question_max = models.IntegerField()
    alignment = models.CharField(max_length=9, choices=ALIGNMENT_CHOICES)
    gai_score = models.CharField(max_length=250)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(999.99)])
    assess_max = models.IntegerField()
    assess_weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(100.00)])
    assess_descript = models.CharField(max_length=200)
    clos = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"GAI: {self.gai} | GA: {self.ga} | Course: {self.course} | Question Max: {self.question_max} | "
                f"Alignment: {self.alignment} | Total Score: {self.total_score} | "
                f"Assess Max: {self.assess_max} | Assess Weight: {self.assess_weight} | GAI Scores: {self.gai_score}")


class AccredReport(models.Model):
    program = models.CharField(max_length=4, choices=PROGRAM_CHOICES)
    term = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    ga = models.CharField(
        max_length=4,
        choices=[(f'GA{i}', f'GA{i}') for i in range(1, 13)]
    )
    gai = models.CharField(
        max_length=4,
        choices=GAI_CHOICES
    )
    assess_type = models.CharField(max_length=15, choices=ASSESSMENT_TYPE_CHOICES)
    quest_text = models.CharField(max_length=400)
    alignment = models.CharField(max_length=9, choices=ALIGNMENT_CHOICES)
    instr_level = models.CharField(max_length=24, choices=[("Introductory", "Introductory"),
                                                           ("Intermediate Development", "Intermediate Development"),
                                                           ("Advanced Application", "Advanced Application")])
    achievement_level = models.DecimalField(max_digits=5, decimal_places=2)
    student_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Program: {self.program} | Term: {self.term} | GA: {self.ga} | GAI: {self.gai} | Assessment Type: "
                f"{self.assess_type} | Question Text: {self.quest_text} | Alignment: {self.alignment} | Instructional "
                f"Level: {self.instr_level} | Achievement Level: {self.achievement_level} | "
                f"Student ID: {self.student_id}")


class AnnualReport(models.Model):
    program = models.CharField(max_length=4, choices=PROGRAM_CHOICES)
    term = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    course = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    ga = models.CharField(
        max_length=4,
        choices=[(f'GA{i}', f'GA{i}') for i in range(1, 13)]
    )
    gai = models.CharField(
        max_length=4,
        choices=GAI_CHOICES
    )
    student_id = models.CharField(max_length=250)
    achievement_level = models.DecimalField(max_digits=5, decimal_places=2)
    assess_type = models.CharField(max_length=15, choices=ASSESSMENT_TYPE_CHOICES)
    instr_comments = models.CharField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Program: {self.program} | Term: {self.term} | Course: {self.course} | GA: {self.ga} | GAI: {self.gai}"
                f" | Achievement Level: {self.achievement_level} | Assessment Type: {self.assess_type} | Instructor "
                f"Comments: {self.instr_comments} | Student ID: {self.student_id}")
    
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_uploaded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
