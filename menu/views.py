from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def menu_list(request):
    """Returns all available menus"""
    all_menus = Menu.objects.all()
    menus = []
    for menu in all_menus:
        if menu.expiration_date is not None:  # Account for NULL values
            if menu.expiration_date >= timezone.now():
                menus.append(menu)

    menus = sorted(menus, key=attrgetter('expiration_date'))
    return render(request, 'menu/menu_list.html', {'menus': menus})


def menu_detail(request, pk):
    """Returns all detailed menu items"""
    try:
        menu = Menu.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """Returns all ingredients that are part of the menu item"""
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/item_detail.html', {'item': item})


def create_new_menu(request):
    """Create new menu item"""
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu_detail', pk=menu.pk)

    form = MenuForm()
    return render(request, 'menu/create_new_menu.html', {'form': form})


def edit_menu(request, pk):
    """Edit existing menu"""
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('menu_detail', pk=pk)
    form = MenuForm(instance=menu)
    return render(request, 'menu/edit_menu.html', {'form': form})


def edit_item(request, pk):
    """edit an item"""
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk=pk)
    form = ItemForm(instance=item)
    return render(request, 'menu/item_edit.html', {'form': form})
