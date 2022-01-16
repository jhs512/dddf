from django.conf import settings

from markets.models import Market


def gen_master(apps, schema_editor):
    if not settings.DEBUG:
        return

    Market(name="언니네옷가게", site_url="https://www.abc1.co.kr", email="test1@test.com", master_id=2).save()
    Market(name="누나네옷가게", site_url="https://www.abc2.co.kr", email="test2@test.com", master_id=3).save()
    Market(name="이모네옷가게", site_url="https://www.abc3.co.kr", email="test3@test.com", master_id=4).save()
