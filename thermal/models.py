from django.db import models


class Geometry(models.Model):
    geometry_id = models.AutoField(primary_key=True)
    project_id = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True, default=None)
    sector = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True, default=None)
    bottom_mark = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=None)
    skeleton_thickness = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=None)
    skeleton_radius_outer = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    skeleton_radius_inner = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    skeleton_transcalency = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    skeleton_resistance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    clamp_lining_thickness = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=None)
    clamp_lining_radius_outer = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    clamp_lining_radius_inner = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    clamp_lining_transcalency = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    clamp_lining_resistance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    air_thickness = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=None)
    air_radius_outer = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    air_radius_inner = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    air_transcalency = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    air_resistance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    insulation_thickness = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=None)
    insulation_radius_outer = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    insulation_radius_inner = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    insulation_transcalency = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    insulation_resistance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    lining_thickness = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=None)
    lining_radius_outer = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    lining_radius_inner = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=None)
    lining_transcalency = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    lining_resistance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    total_resistance = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def fields_name(self):
        return [field.name for field in self._meta.get_fields()[:-2]]

    def __str__(self):
        return "%s %s" % (self.geometry_id, self.sector)

    class Meta:
        verbose_name = 'Участок'


class Data(models.Model):
    temperature_gas = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True, default=None)
    density_gas = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, default=None)
    kinematic_viscosity = models.DecimalField(max_digits=9, decimal_places=8, blank=True, null=True, default=None)
    heat_output_gas = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True, default=None)

    def __str__(self):
        return "%s" % self.temperature_gas

    class Meta:
        verbose_name = 'Расчет-температуры'


class Condition(models.Model):
    condition_id = models.AutoField(primary_key=True)
    volume_gas = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True, default=None)
    current_temperature_gas = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True, default=None)
    current_temperature = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True, default=None)

    def __str__(self):
        return "%s" % self.volume_gas

    class Meta:
        verbose_name = 'Текущие данные температуры'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    condition = models.ForeignKey(Condition, default=0, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s" % self.project_id

    class Meta:
        verbose_name = 'Номер проекта'
