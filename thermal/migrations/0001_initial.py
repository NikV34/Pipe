# Generated by Django 2.1a1 on 2018-06-02 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('condition_id', models.AutoField(primary_key=True, serialize=False)),
                ('volume_gas', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=4, null=True)),
                ('current_temperature_gas', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=3, null=True)),
                ('current_temperature', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=2, null=True)),
            ],
            options={
                'verbose_name': 'Текущие данные температуры',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature_gas', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=3, null=True)),
                ('density_gas', models.DecimalField(blank=True, decimal_places=3, default=None, max_digits=4, null=True)),
                ('kinematic_viscosity', models.DecimalField(blank=True, decimal_places=8, default=None, max_digits=9, null=True)),
                ('heat_output_gas', models.DecimalField(blank=True, decimal_places=3, default=None, max_digits=4, null=True)),
            ],
            options={
                'verbose_name': 'Расчет-температуры',
            },
        ),
        migrations.CreateModel(
            name='Geometry',
            fields=[
                ('geometry_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_id', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=4, null=True)),
                ('sector', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=2, null=True)),
                ('bottom_mark', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True)),
                ('skeleton_thickness', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=6, null=True)),
                ('skeleton_radius_outer', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('skeleton_radius_inner', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('skeleton_transcalency', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('skeleton_resistance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('clamp_lining_thickness', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=6, null=True)),
                ('clamp_lining_radius_outer', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('clamp_lining_radius_inner', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('clamp_lining_transcalency', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('clamp_lining_resistance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('air_thickness', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=6, null=True)),
                ('air_radius_outer', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('air_radius_inner', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('air_transcalency', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('air_resistance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('insulation_thickness', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=6, null=True)),
                ('insulation_radius_outer', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('insulation_radius_inner', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('insulation_transcalency', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('insulation_resistance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('lining_thickness', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=6, null=True)),
                ('lining_radius_outer', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('lining_radius_inner', models.DecimalField(blank=True, decimal_places=0, default=None, max_digits=5, null=True)),
                ('lining_transcalency', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('lining_resistance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('total_resistance', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Участок',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('condition', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='thermal.Condition')),
            ],
            options={
                'verbose_name': 'Номер проекта',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('result', models.AutoField(primary_key=True, serialize=False)),
                ('condition', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='thermal.Condition')),
            ],
            options={
                'verbose_name': 'Текущие данные температуры',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='result',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='thermal.Result'),
        ),
    ]
