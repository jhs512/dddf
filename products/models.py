from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from markets.models import Market
from qna.models import Question


# unique=True 처리
class ProductCategory(models.Model):
    name = models.CharField('이름', max_length=50, unique=True)


class Product(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)

    is_deleted = models.BooleanField('삭제여부', default=False)
    delete_date = models.DateTimeField('삭제날짜', null=True, blank=True)

    market = models.ForeignKey(Market, on_delete=models.DO_NOTHING)
    name = models.CharField('상품명(내부용)', max_length=100)
    display_name = models.CharField('상품명(노출용)', max_length=100)

    price = models.PositiveIntegerField('권장판매가')
    sale_price = models.PositiveIntegerField('실제판매가')

    is_hidden = models.BooleanField('노출여부', default=False)
    is_sold_out = models.BooleanField('품절여부', default=False)

    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING)

    hit_count = models.PositiveIntegerField('조회수', default=0)
    review_count = models.PositiveIntegerField('리뷰수', default=0)
    review_point = models.PositiveIntegerField('리뷰평점', default=0)

    questions = GenericRelation(Question, related_query_name="question")

    # 임시 함수, 리팩토링 필요
    def thumb_img_url(self):
        img_name = self.category.name

        img_name += '2' if self.id % 2 == 0 else ''

        return f"https://raw.githubusercontent.com/jhs512/mbly-img/master/{img_name}.jpg"

    # 임시 함수, 리팩토링 필요
    def colors(self):
        colors = []
        # 상품리스트 페이지에서 이 함수를 호출하면, 실제 쿼리가 발생하지 않습니다.
        # 그 이유는 상품리스트를 불러올 때 prefetch_related 를 사용해서 미리 로딩했기 때문입니다.
        product_reals = self.product_reals.all()
        for product_real in product_reals:
            colors.append(product_real.option_2_name)

        html = ''

        for color in set(colors):
            rgb_color = ProductReal.rgb_color_from_color_name(color)

            html += f"""<span style="width:10px; height:10px; display:inline-block; border-radius:50%; margin:0 3px; background-color:#{rgb_color};"></span>"""

        return html


class ProductReal(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_reals")
    option_1_type = models.CharField('옵션1 타입', max_length=10, default='SIZE')
    option_1_name = models.CharField('옵션1 이름(내부용)', max_length=50)
    option_1_display_name = models.CharField('옵션1 이름(고객용)', max_length=50)
    option_2_type = models.CharField('옵션2 타입', max_length=10, default='COLOR')
    option_2_name = models.CharField('옵션2 이름(내부용)', max_length=50)
    option_2_display_name = models.CharField('옵션2 이름(고객용)', max_length=50)
    option_3_type = models.CharField('옵션3 타입', max_length=10, default='', blank=True)
    option_3_name = models.CharField('옵션3 이름(내부용)', max_length=50, default='', blank=True)
    option_3_display_name = models.CharField('옵션3 이름(고객용)', max_length=50, default='', blank=True)
    is_sold_out = models.BooleanField('품절여부', default=False)
    is_hidden = models.BooleanField('노출여부', default=False)
    add_price = models.IntegerField('추가가격', default=0)
    stock_quantity = models.PositiveIntegerField('재고개수', default=0)  # 품절일때 유용함

    @classmethod
    def rgb_color_from_color_name(cls, color):
        if color == '레드':
            rgb_color = 'ff0000'
        elif color == '그린':
            rgb_color = '008000'
        elif color == '블루':
            rgb_color = '0000ff'
        elif color == '핑크':
            rgb_color = 'FFC0CB'
        elif color == '와인':
            rgb_color = '722F37'
        else:
            rgb_color = 'ffffff'

        return rgb_color

    def rgb_color(self):
        return ProductReal.rgb_color_from_color_name(self.option_2_name)