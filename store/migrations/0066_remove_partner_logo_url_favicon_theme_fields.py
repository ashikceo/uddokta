# Generated manually - remove deprecated partner fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0065_partner_theme_sitelogo_site_primary_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='logo_url',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='primary_color',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='secondary_color',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='custom_css',
        ),
        migrations.AlterField(
            model_name='partner',
            name='theme',
            field=models.CharField(blank=True, choices=[('default', 'Default Red'), ('ocean_blue', 'Ocean Blue'), ('forest_green', 'Forest Green'), ('royal_purple', 'Royal Purple'), ('sunset_orange', 'Sunset Orange'), ('teal', 'Teal'), ('dark_mode', 'Dark Mode'), ('rose_pink', 'Rose Pink'), ('amber', 'Amber'), ('slate_gray', 'Slate Gray')], default='', max_length=30, verbose_name='Store Theme', help_text='Override site theme for this store. Leave empty to use site default.'),
        ),
    ]
