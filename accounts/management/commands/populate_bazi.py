from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = '為現有用戶批量計算並填充八字資料'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='每批處理的用戶數量',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='僅顯示將要處理的用戶數量，不實際執行',
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        dry_run = options['dry_run']

        # 查詢需要填充八字的用戶：有生日但沒有八字年柱
        users_to_update = CustomUser.objects.filter(
            gregorian_birth_date__isnull=False,
            bazi_year__isnull=True
        ) | CustomUser.objects.filter(
            gregorian_birth_date__isnull=False,
            bazi_year=''
        )

        total_users = users_to_update.count()

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'將處理 {total_users} 個用戶的八字資料 (dry run)'
                )
            )
            return

        if total_users == 0:
            self.stdout.write(
                self.style.SUCCESS('沒有需要填充八字資料的用戶')
            )
            return

        self.stdout.write(
            f'開始處理 {total_users} 個用戶的八字資料...'
        )

        processed = 0
        updated = 0

        # 分批處理
        for i in range(0, total_users, batch_size):
            batch = users_to_update[i:i + batch_size]

            for user in batch:
                try:
                    # 調用 save() 方法來計算八字
                    user.save()
                    updated += 1
                    processed += 1

                    if processed % 100 == 0:
                        self.stdout.write(
                            f'已處理 {processed}/{total_users} 個用戶'
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'處理用戶 {user.email} 時發生錯誤: {str(e)}'
                        )
                    )
                    processed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'處理完成！成功更新 {updated}/{total_users} 個用戶的八字資料'
            )
        )