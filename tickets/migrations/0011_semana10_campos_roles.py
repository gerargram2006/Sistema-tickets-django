import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0010_semana10_prioridad_roles"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ticket",
            old_name="fecha_apertura",
            new_name="creado",
        ),
        migrations.RenameField(
            model_name="ticket",
            old_name="propietario",
            new_name="creado_por",
        ),
        migrations.AlterField(
            model_name="categoria",
            name="peso",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="impacto",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "Muy bajo"), (2, "Bajo"), (3, "Medio"), (4, "Alto"), (5, "Crítico")],
                default=1,
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)],
            ),
        ),
        migrations.RemoveField(
            model_name="ticket",
            name="formula_postfija",
        ),
    ]
