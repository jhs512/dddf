# Generated by Django 4.0.1 on 2022-01-11 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제여부')),
                ('delete_date', models.DateTimeField(blank=True, null=True, verbose_name='삭제날짜')),
                ('name', models.CharField(max_length=100, verbose_name='상품명(내부용)')),
                ('display_name', models.CharField(max_length=100, verbose_name='상품명(노출용)')),
                ('price', models.PositiveIntegerField(verbose_name='권장판매가')),
                ('sale_price', models.PositiveIntegerField(verbose_name='실제판매가')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='노출여부')),
                ('is_sold_out', models.BooleanField(default=False, verbose_name='품절여부')),
                ('hit_count', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('review_count', models.PositiveIntegerField(default=0, verbose_name='리뷰수')),
                ('review_point', models.PositiveIntegerField(default=0, verbose_name='리뷰평점')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='이름')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='갱신날짜')),
                ('option_1_type', models.CharField(default='SIZE', max_length=10, verbose_name='옵션1 타입')),
                ('option_1_name', models.CharField(max_length=50, verbose_name='옵션1 이름(내부용)')),
                ('option_1_display_name', models.CharField(max_length=50, verbose_name='옵션1 이름(고객용)')),
                ('option_2_type', models.CharField(default='COLOR', max_length=10, verbose_name='옵션2 타입')),
                ('option_2_name', models.CharField(max_length=50, verbose_name='옵션2 이름(내부용)')),
                ('option_2_display_name', models.CharField(max_length=50, verbose_name='옵션2 이름(고객용)')),
                ('option_3_type', models.CharField(blank=True, default='', max_length=10, verbose_name='옵션3 타입')),
                ('option_3_name', models.CharField(blank=True, default='', max_length=50, verbose_name='옵션3 이름(내부용)')),
                ('option_3_display_name', models.CharField(blank=True, default='', max_length=50, verbose_name='옵션3 이름(고객용)')),
                ('is_sold_out', models.BooleanField(default=False, verbose_name='품절여부')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='노출여부')),
                ('add_price', models.IntegerField(default=0, verbose_name='추가가격')),
                ('stock_quantity', models.PositiveIntegerField(default=0, verbose_name='재고개수')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reals', to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='markets.market'),
        ),
    ]
