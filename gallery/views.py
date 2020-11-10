# -*- coding: utf-8 -*-
from django.shortcuts import render
from py3pin.Pinterest import Pinterest
from django.db import IntegrityError
import os
from django.shortcuts import render
from pinlery.settings import BASE_DIR
from django.shortcuts import redirect
from django.views import generic
from django.core.paginator import Paginator
from .models import Board, Section, Pin

pinterest = Pinterest(email='nennertrennen@gmail.com',
                      password='PIZa69pINTERES',
                      username='nennertrennen',
                      cred_root=os.path.join(BASE_DIR, 'cookies'))
#pinterest.login()

def showcase(request, section_slug):
    section = Section.objects.get(slug=section_slug)
    section_id = int(section.id_pinterest)
    pins = Pin.objects.filter(section__id_pinterest=section_id)
    paginator = Paginator(pins, 15)
    page = request.GET.get('page')
    pins = paginator.get_page(page)
    return render(request, 'gallery/showcase.html', {'pins': pins, 'section_title': section.title_custom_split, 'section_slug': section.slug_custom_split})

def create_boards(request):
    boards = pinterest.boards(username='nennertrennen')
    for board in boards:
        target_board_id = int(board['id'])
        # I need to make a slug!!!
        new_board = Board(title=board['name'], id_pinterest=target_board_id)
        try:
            new_board.save()
        except IntegrityError:
            continue


def create_sections(request):
    active_boards = Board.objects.filter(active=True)
    for board in active_boards:
        target_board_id = str(int(board.id_pinterest))
        sections = pinterest.get_board_sections(board_id=target_board_id)
        while sections:
            for section in sections:
                section_id = int(section['id'])
                new_section = Section(title=section['title'], id_pinterest=section_id, board=board, slug=section["slug"])
                try:
                    new_section.save()
                except IntegrityError:
                    continue
            sections = pinterest.get_board_sections(board_id=target_board_id, reset_bookmark=True)


def create_pins(request):
    active_sections = Section.objects.filter(active=True)
    for section in active_sections:
        target_section_id = str(int(section.id_pinterest))
        pins = pinterest.get_section_pins(section_id=target_section_id)
        while pins:
            for pin in pins:
                if len(pin["title"]) < 2 and len(pin["description"]) < 2:
                    pin_title = "Untitled"
                elif len(pin["title"]) < 2:
                    pin_title = pin["description"]
                else:
                    pin_title = pin["title"]
                pin_id = int(pin['id'])
                pin_color = pin['dominant_color']
                new_pin = Pin(id_pinterest=pin_id, title=pin_title, section=section,
                              image_url=pin["images"]["orig"]["url"],
                              small_image_url=pin["images"]["236x"]["url"], color=pin_color)
                try:
                    new_pin.save()
                except IntegrityError:
                    continue
            pins = pinterest.get_section_pins(section_id=target_section_id, reset_bookmark=True)

def masonry(request):
    return render(request, 'gallery/masonry.html')

class section_list(generic.ListView):
    model = Section

    def get_queryset(self):
        return Section.objects.filter(active=True)


class test(generic.ListView):
    model = Section

    def get_queryset(self):
        return Section.objects.filter(active=True)

