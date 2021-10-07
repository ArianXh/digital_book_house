from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

from django.urls import reverse
from viewflow.fields import CompositeKey


class AccountsClen(models.Model):
    c_ime = models.CharField(max_length=100)
    c_prezime = models.CharField(max_length=100)
    c_adresa = models.CharField(max_length=100)
    c_email = models.CharField(max_length=100)
    datum_zaclenuvanje = models.DateTimeField()
    pass_clen = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'accounts_clen'


class AccountsUser(models.Model):
    user_ptr = models.OneToOneField('AuthUser', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'accounts_user'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Avtor(models.Model):
    avtorid = models.AutoField(primary_key=True)
    aemail = models.CharField(max_length=100)
    aime = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'avtor'


class Biblioteka(models.Model):
    bibliotekaid = models.AutoField(primary_key=True)
    badresa = models.CharField(max_length=100)
    bime = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'biblioteka'


class Bibliotekar(models.Model):
    bibliotekarid = models.OneToOneField('Lugje', models.DO_NOTHING, db_column='bibliotekarid', primary_key=True)
    bibliotekaid = models.ForeignKey(Biblioteka, models.DO_NOTHING, db_column='bibliotekaid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bibliotekar'


class Clen(models.Model):
    clenskibr = models.OneToOneField('Lugje', on_delete=models.CASCADE, db_column='clenskibr', primary_key=True)
    datumzaclenuvanje = models.DateField()
    passwordclen = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'clen'


    def get_absolute_url(self):
        return reverse('clen-detail', args=[str(self.clenskibr)])

    def __str__(self):
        return self.clenskibr




class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dodava(models.Model):
    bibliotekarid = models.OneToOneField(Bibliotekar, models.DO_NOTHING, db_column='bibliotekarid', primary_key=True)
    knigaid = models.ForeignKey('Knigi', models.DO_NOTHING, db_column='knigaid')

    class Meta:
        managed = False
        db_table = 'dodava'
        unique_together = (('bibliotekarid', 'knigaid'),)


class Instancakniga(models.Model):

    knigaid = models.OneToOneField('Knigi', models.DO_NOTHING, db_column='knigaid', primary_key=True)
    seriskibr = models.IntegerField()
    id = CompositeKey(columns=['knigaid', 'seriskibr'])
    istatus = models.CharField(max_length=1000)
    bibliotekaid = models.ForeignKey(Biblioteka, models.DO_NOTHING, db_column='bibliotekaid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instancakniga'
        unique_together = (('knigaid', 'seriskibr'),)


class ItelBroj(models.Model):
    izdavacid = models.OneToOneField('Izdavac', models.DO_NOTHING, db_column='izdavacid', primary_key=True)
    ltel_broj = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'itel_broj'
        unique_together = (('izdavacid', 'ltel_broj'),)





class Kategorija(models.Model):
    kategorijaid = models.AutoField(primary_key=True)
    naslovkategorija = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'kategorija'


class Klasificira(models.Model):
    kategorijaid = models.OneToOneField(Kategorija, models.DO_NOTHING, db_column='kategorijaid', primary_key=True)
    knigaid = models.ForeignKey('Knigi', models.DO_NOTHING, db_column='knigaid')

    class Meta:
        managed = False
        db_table = 'klasificira'
        unique_together = (('kategorijaid', 'knigaid'),)


class Izdavac(models.Model):
    izdavacid = models.AutoField(primary_key=True)
    iadresa = models.CharField(max_length=100, blank=True, null=True)
    iime = models.CharField(max_length=100)
    iemail = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'izdavac'


class Knigi(models.Model):
    knigaid = models.AutoField(primary_key=True)
    naslov = models.CharField(max_length=100)
    kformat = models.CharField(max_length=100)
    kopis = models.CharField(max_length=1000)
    izdavacid = models.ForeignKey(Izdavac, models.DO_NOTHING, db_column='izdavacid')

    class Meta:
        managed = False
        db_table = 'knigi'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.knigaid)])


    def __str__(self):
        self.naslov


class LtelBroj(models.Model):
    lugjeid = models.OneToOneField('Lugje', models.DO_NOTHING, db_column='lugjeid', primary_key=True)
    ltel_broj = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ltel_broj'
        unique_together = (('lugjeid', 'ltel_broj'),)


class Lugje(models.Model):
    lugjeid = models.AutoField(primary_key=True)
    ime = models.CharField(max_length=100)
    prezime = models.CharField(max_length=100)
    adresa = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'lugje'

    def get_absolute_url(self):
        return reverse('clen-detail', args=[str(self.lugjeid)])

class Napisal(models.Model):
    avtorid = models.OneToOneField(Avtor, models.DO_NOTHING, db_column='avtorid', primary_key=True)
    knigaid = models.ForeignKey(Knigi, models.DO_NOTHING, db_column='knigaid')

    class Meta:
        managed = False
        db_table = 'napisal'
        unique_together = (('avtorid', 'knigaid'),)

    def __init__(self, avtorid, knigaid):
        self.avtorid = avtorid
        self.knigaid = knigaid

    def get_avtor(self, avtor, kniga):
        pass

class Ocena(models.Model):
    ocenaid = models.AutoField(primary_key=True)
    ocenka = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    komentar = models.CharField(max_length=1000, blank=True, null=True)
    avtorid = models.ForeignKey(Avtor, models.DO_NOTHING, db_column='avtorid')
    knigaid = models.ForeignKey(Knigi, models.DO_NOTHING, db_column='knigaid')
    clenskibr = models.ForeignKey(Clen, models.DO_NOTHING, db_column='clenskibr')

    class Meta:
        managed = False
        db_table = 'ocena'


class Pozajmica(models.Model):
    pozajmicaid = models.AutoField(primary_key=True)
    pstatus = models.CharField(max_length=1000)
    pocetokdatum = models.DateField()
    krajdatum = models.DateField()
    knigaid = models.ForeignKey(Instancakniga, models.DO_NOTHING, db_column='knigaid')
    seriskibr = models.IntegerField()
    fk = CompositeKey(columns=['knigaid', 'seriskibr'])

    class Meta:
        managed = False
        db_table = 'pozajmica'


class Rezervacija(models.Model):
    rezervacijaid = models.AutoField(primary_key=True)
    rstatus = models.CharField(max_length=1000)
    dennarezervacija = models.DateField()
    pozajmicaid = models.ForeignKey(Pozajmica, models.DO_NOTHING, db_column='pozajmicaid')
    bibliotekarid = models.ForeignKey(Bibliotekar, models.DO_NOTHING, db_column='bibliotekarid')
    knigaid = models.ForeignKey(Knigi, models.DO_NOTHING, db_column='knigaid')
    clenskibr = models.ForeignKey(Clen, models.DO_NOTHING, db_column='clenskibr')

    class Meta:
        managed = False
        db_table = 'rezervacija'


class TestEmailValiden(models.Model):
    emailid = models.IntegerField(primary_key=True)
    aemail = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'test_email_validen'




#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40, null=True)
    branch = models.CharField(max_length=40, null=True)

    # used in issue book
    def __str__(self):
        return self.user.first_name + '[' + str(self.enrollment) + ']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id






def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)


    def __str__(self):
        return self.enrollment

#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################