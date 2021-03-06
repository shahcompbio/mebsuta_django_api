# Generated by Django 3.1.7 on 2021-03-04 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_id', models.CharField(max_length=15)),
                ('microscope_image_filename', models.CharField(max_length=100)),
                ('microscope_image_url', models.CharField(max_length=150)),
                ('library_id', models.CharField(max_length=15)),
                ('chip_row', models.IntegerField()),
                ('chip_column', models.IntegerField()),
                ('condition', models.CharField(max_length=5)),
                ('pick_met', models.CharField(max_length=5)),
                ('cellenone_image_filename', models.CharField(max_length=100)),
                ('cellenone_image_url', models.CharField(max_length=175)),
                ('cellenone_background_filename', models.CharField(max_length=100)),
                ('cellenone_background_url', models.CharField(max_length=175)),
                ('X', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Y', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Diameter', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Elongation', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Circularity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Intensity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ejection_zone_boundary', models.IntegerField()),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('jira_ticket', models.CharField(default='', max_length=10)),
                ('sample_id', models.CharField(default='', max_length=25)),
                ('isDebris', models.BooleanField(default=False)),
                ('annotation', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_id', models.CharField(max_length=50)),
                ('num_cells', models.IntegerField()),
                ('num_annotated', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Mebsuta_Users',
            fields=[
                ('user_id', models.CharField(default='', max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Debris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_id', models.CharField(max_length=15)),
                ('cell_id', models.CharField(max_length=15)),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('isDebris', models.BooleanField(default=False)),
                ('Cell_Image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='debris', to='mebsuta_api.cell_image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mebsuta_api.mebsuta_users')),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_id', models.CharField(max_length=500)),
                ('cell_id', models.CharField(max_length=500)),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('annotation', models.CharField(max_length=50)),
                ('Cell_Image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rel_annotation', to='mebsuta_api.cell_image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mebsuta_api.mebsuta_users')),
            ],
        ),
    ]
