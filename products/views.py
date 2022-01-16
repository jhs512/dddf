from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from products.models import Product, ProductCategory
from qna.forms import QuestionForm
from qna.models import Question


def product_list(request: HttpRequest):
    product_cate_items = ProductCategory.objects.all()

    search_keyword = request.GET.get('search_keyword', '')
    category_item_id = request.GET.get('category_item_id', '')
    category_item_name, = (product_cate_item.name for product_cate_item in product_cate_items if
                           product_cate_item.id == int(category_item_id)) if category_item_id else tuple([''])
    page = request.GET.get('page', '1')

    # n+1 문제 해결
    products: QuerySet = Product \
        .objects \
        .select_related('category') \
        .prefetch_related('product_reals') \
        .order_by('-id')

    if search_keyword:
        products = products.filter(display_name__icontains=search_keyword)

    if category_item_id:
        products = products.filter(category=category_item_id)

    paginator = Paginator(products, 8)  # 페이지당 8개씩 보여주기
    products = paginator.get_page(page)

    return render(request, "products/product_list.html", {
        "products": products,
        "product_cate_items": product_cate_items,
        "category_item_name": category_item_name
    })


def _product_detail_data(request: HttpRequest, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_reals = product.product_reals.order_by('option_1_display_name', 'option_2_display_name')
    questions = product.questions.order_by('-id')

    form_name = request.POST.get('form_name', '')

    question_create_form = QuestionForm(request.POST if form_name == 'question_create_form' else None)

    return {
        "product": product,
        "product_reals": product_reals,
        "questions": questions,
        "question_create_form": question_create_form,
    }


def product_detail(request: HttpRequest, product_id):
    context = _product_detail_data(request, product_id)

    return render(request, "products/product_detail.html", context)


@login_required
def question_create(request: HttpRequest, product_id):
    context = _product_detail_data(request, product_id)
    product: Product = context['product']

    question_create_form = QuestionForm(request.POST)

    if question_create_form.is_valid():
        question = question_create_form.save(commit=False)
        question.content_type = ContentType.objects.get_for_model(product)
        question.object_id = product.id
        question.user = request.user
        question.save()
        messages.success(request, "질문이 등록되었습니다.")

        return redirect("products:detail", product_id=product.id)

    context['question_create_form'] = question_create_form

    return render(request, "products/product_detail.html", context)


@login_required
def question_delete(request: HttpRequest, product_id, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.user:
        raise exceptions.PermissionDenied()

    question.delete()

    messages.success(request, f"{product_id}번 질문이 삭제되었습니다.")

    return redirect("products:detail", product_id=product_id)


@login_required
def question_modify(request: HttpRequest, product_id, question_id):
    context = _product_detail_data(request, product_id)

    question = get_object_or_404(Question, id=question_id)
    context['question'] = question

    if request.user != question.user:
        raise exceptions.PermissionDenied()

    if request.method == "POST":
        question_modify_form = QuestionForm(request.POST, instance=question)

        if question_modify_form.is_valid():
            question_modify_form.save()
            messages.success(request, "질문이 수정되었습니다.")
            return redirect("products:detail", product_id=product_id)
    else:
        question_modify_form = QuestionForm(None, instance=question)

    context['question_modify_form'] = question_modify_form

    return render(request, "products/product_detail.html", context)
