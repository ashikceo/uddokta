from django.core.management.base import BaseCommand
from django.db import transaction
from store.models import Product, MedicineProduct


class Command(BaseCommand):
    help = 'Migrate medicine products from Product model to MedicineProduct model and delete originals'

    def add_arguments(self, parser):
        parser.add_argument('--partner-id', type=int, default=16, help='Partner ID to migrate products from')

    def handle(self, *args, **options):
        partner_id = options['partner_id']

        products = Product.objects.filter(partner_id=partner_id).exclude(medicine_brand_name='')
        total = products.count()

        if total == 0:
            self.stdout.write(self.style.WARNING('No medicine products found for this partner.'))
            return

        self.stdout.write(f'Found {total} medicine products for partner id={partner_id}')

        confirmed = input(f'This will DELETE {total} Product records after migrating to MedicineProduct. Continue? [y/N]: ')
        if confirmed.lower() != 'y':
            self.stdout.write(self.style.WARNING('Cancelled.'))
            return

        migrated = 0
        errors = []
        batch = []
        ids_to_delete = []

        for i, product in enumerate(products.iterator(chunk_size=500)):
            mp = MedicineProduct(
                brand_name=product.medicine_brand_name or '',
                generic_name=product.medicine_generic_name or '',
                strength=product.medicine_strength or '',
                dosage_form=product.medicine_dosage_form or '',
                sku=product.sku or '',
                price=product.price,
                stock=product.stock,
                description=product.description or '',
                is_approved=True,
                requested_by=None,
            )
            batch.append(mp)
            ids_to_delete.append(product.id)

            if len(batch) >= 200:
                try:
                    MedicineProduct.objects.bulk_create(batch, ignore_conflicts=True)
                except Exception as e:
                    errors.append(f'Batch at {i}: {e}')
                    for mp_item in batch:
                        try:
                            mp_item.save()
                            migrated += 1
                        except Exception as e2:
                            errors.append(f'  SKU {mp_item.sku}: {e2}')
                else:
                    migrated += len(batch)
                batch = []

            if (i + 1) % 1000 == 0:
                self.stdout.write(f'  Processed {i + 1}/{total}...')

        if batch:
            try:
                MedicineProduct.objects.bulk_create(batch, ignore_conflicts=True)
            except Exception as e:
                errors.append(f'Final batch: {e}')
                for mp_item in batch:
                    try:
                        mp_item.save()
                        migrated += 1
                    except Exception as e2:
                        errors.append(f'  SKU {mp_item.sku}: {e2}')
            else:
                migrated += len(batch)

        self.stdout.write(f'Created {migrated} MedicineProduct records.')

        if errors:
            self.stdout.write(self.style.ERROR(f'{len(errors)} errors during creation:'))
            for err in errors[:20]:
                self.stdout.write(self.style.ERROR(f'  {err}'))
            if len(errors) > 20:
                self.stdout.write(self.style.ERROR(f'  ... and {len(errors) - 20} more'))

        self.stdout.write(f'Deleting {len(ids_to_delete)} original Product records...')
        try:
            with transaction.atomic():
                Product.objects.filter(id__in=ids_to_delete).delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {len(ids_to_delete)} Product records.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error deleting products: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Migrated {migrated} / {total} medicine products.'))
