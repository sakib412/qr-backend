from django.db import models
from django.conf import settings
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO
import qrcode

User = settings.AUTH_USER_MODEL
COURSE_CODE = [
    ('CSE336', 'CSE336'),
    ('CSE335', 'CSE335'),
    ('CSE334', 'CSE334'),
    ('CSE332', 'CSE332'),
    ('CSE331', 'CSE331'),
]


def qr_code_path(instance, filename):
    # upload path 'root/avatar/<id>-alo-<filename>
    return "qr_code/{0}".format(filename)


class Attendence(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='teacher')
    section = models.CharField(max_length=255)
    date = models.DateField()
    course_code = models.CharField(max_length=255, choices=COURSE_CODE)
    qr = models.ImageField(upload_to=qr_code_path, blank=True)
    student = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Teacher cannot add attendence in same day with same section and same course.
        unique_together = ('section', 'date', 'course_code')

    def __str__(self):
        return self.section

    def save(self, *args, **kwargs):
        qr_data = {
            "section": self.section,
            "course_code": self.course_code,
            "date": self.date.strftime('%Y-%m-%d')
        }
        qr_image = qrcode.make(qr_data)
        qr_offset = Image.new('RGB', (450, 450), 'white')
        draw = ImageDraw.Draw(qr_image)
        qr_offset.paste(qr_image)
        file_name = f'{self.course_code}_{self.section}_({self.date}).png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)


class Student(models.Model):
    studentID = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)