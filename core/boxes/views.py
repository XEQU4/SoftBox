import contextlib
import random
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Box, Comment

User = get_user_model()


def main_view(request):
    context = {
        'show_info_modal': False,
        'show_error_modal': False,
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('start')

        if User.objects.filter(username=username).exists():
            context['show_error_modal'] = True
        else:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            login(request, user)
            return redirect('start')

    if request.GET.get('info') == '1':
        context['show_info_modal'] = True

    return render(request, 'main.html', context)


@login_required
def start_view(request):
    with contextlib.suppress(KeyError):
        del request.session['draft_message']

    user = request.user

    show_created_modal = False
    created_box_number = None

    opened_recently = (
            user.last_box_opened and
            user.last_box_opened >= timezone.now() - timedelta(hours=24)
    )

    created_recently = (
            user.last_box_created and
            user.last_box_created >= timezone.now() - timedelta(hours=24)
    )

    if 'created_box_number' in request.session:
        show_created_modal = True
        created_box_number = request.session['created_box_number']
        del request.session['created_box_number']

    return render(request, 'start.html', {
        'show_created_modal': show_created_modal,
        'created_box_number': created_box_number,
        'opened_recently': opened_recently,
        'created_recently': created_recently,
    })


@login_required
def create_message_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        request.session['draft_message'] = message
        return redirect('choose_category')

    return render(request, 'create_message.html')


@login_required
def choose_category_view(request):
    message = request.session.get('draft_message')

    if not message:
        return redirect('create_message')

    if request.method == 'POST':
        category = request.POST.get('category')

        # Генерим уникальный номер коробки
        count = Box.objects.filter(category=category).count()
        while True:
            if count <= 100:
                number = random.randint(1, 100)
            elif count <= 1000:
                number = random.randint(1, 1000)
            elif count <= 10000:
                number = random.randint(1, 10000)
            else:
                number = random.randint(1, 100000)

            if not Box.objects.filter(number=number).exists():
                break

        box = Box.objects.create(
            number=number,
            category=category,
            text=message,
            user=request.user
        )

        request.user.last_box_created = datetime.now()
        request.user.save(update_fields=['last_box_created'])

        del request.session['draft_message']
        request.session['created_box_number'] = box.number

        return redirect('start')

    return render(request, 'choose_category.html')


@login_required
def profile_view(request):
    user = request.user

    context = {
        'created_boxes_count': Box.objects.filter(user=user).count(),
        'opened_boxes_count': user.opened_boxes.count(),
    }

    return render(request, 'profile.html', context)


@login_required
def profile_opened_boxes_view(request):
    boxes = (
        request.user.opened_boxes
        .all()
        .annotate(comments_count=Count('comments'))
        .order_by('-created_at')
    )

    context = {
        'boxes': boxes
    }

    return render(request, 'profile_opened_boxes.html', context)


@login_required
def profile_created_boxes_view(request):
    boxes = (
        Box.objects
        .filter(user=request.user)
        .annotate(comments_count=Count('comments'))
        .order_by('-created_at')
    )

    context = {
        'boxes': boxes
    }

    return render(request, 'profile_created_boxes.html', context)


@login_required
def box_detail_view(request, number):
    print(number)

    box = get_object_or_404(
        Box.objects.annotate(comments_count=Count('comments')),
        number=number
    )

    # отмечаем что пользователь открыл бокс
    if request.user not in box.opened_by.all():
        box.opened_by.add(request.user)

    if request.method == "POST":
        text = request.POST.get("comment_text")

        if text:
            Comment.objects.create(
                box=box,
                user=request.user,
                text=text
            )
            return redirect('box_detail', number=number)

    comments = box.comments.select_related('user').order_by('-created_at')

    context = {
        'box': box,
        'comments': comments
    }

    return render(request, 'box_detail.html', context)


@login_required
def random_box_view(request):
    opened_recently = (
        request.user.last_box_opened and
        request.user.last_box_opened >= timezone.now() - timedelta(hours=24)
    )

    if opened_recently:
        return render(request, "random_box.html", {
            "opened_recently": True
        })

    if request.method == "POST":
        category = request.POST.get("category")

        boxes = Box.objects.filter(
            category=category
        ).exclude(
            opened_by=request.user
        ).exclude(
            user_id=request.user
        )

        if not boxes.exists():
            return render(request, "random_box.html", {
                "opened_recently": False,
                "no_boxes_left": True
            })

        box = random.choice(list(boxes))
        box.opened_by.add(request.user)

        request.user.last_box_opened = timezone.now()
        request.user.save(update_fields=["last_box_opened"])

        return redirect("box_detail", number=box.number)

    return render(request, "random_box.html", {
        "opened_recently": False
    })
