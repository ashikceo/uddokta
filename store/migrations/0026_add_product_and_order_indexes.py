from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_customorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], db_index=True, default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('refunded', 'Refunded')], db_index=True, default='unpaid', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='session_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created']},
        ),
    ]
