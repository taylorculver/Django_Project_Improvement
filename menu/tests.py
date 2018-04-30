from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from menu.models import Menu, Item, Ingredient
from menu.forms import MenuForm, ItemForm

user = User.objects.get(id=1)


class MyTests(TestCase):
    """all of the unittests"""

    def setUp(self):
        """create an instance in the database"""
        self.ingredient = Ingredient.objects.create(
            name="Pepperoni"
        )
        self.item = Item(
            name="Pizza",
            description="Round and delicious",
            chef=user,
        )
        self.item.save()
        self.item.ingredients.add(self.ingredient)

        self.menu = Menu(
            season="YearLong",
            expiration_date=timezone.now() + timezone.timedelta(days=1)
        )
        self.menu.save()
        self.menu.items.add(self.item)

    def test_models_creation(self):
        """Test creation of the model with sample data above"""
        now = timezone.now()
        self.assertLess(self.item.created_date, now)
        self.assertLess(self.menu.created_date, now)
        self.assertIn(self.ingredient, self.item.ingredients.all())
        self.assertIn(self.item, self.menu.items.all())
        self.assertEqual(user, self.item.chef)

    def test_menu_list_view(self):
        """Test the rendering of the menu list template"""
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/menu_list.html')
        self.assertContains(resp, self.menu.season)

    def test_menu_detail_view(self):
        """Test the rendering of the menu detail view"""
        resp = self.client.get(reverse('menu_detail',
                                       kwargs={'pk': self.menu.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, self.menu.season)

    def test_item_detail_view(self):
        """Test the rendering of the item detail view"""
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.item.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/item_detail.html')
        self.assertContains(resp, self.item.name)

    def test_create_new_menu_view_get(self):
        """Test the rendering of the create new menu view"""
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/create_new_menu.html')
        self.assertContains(resp, "Add New Menu")

    def test_create_new_menu_view_post(self):
        """Test the posting of data from the create new menu view"""
        expiration_date = timezone.now() + timezone.timedelta(days=2)

        self.client.post('/menu/new/', data={
            'expiration_date': expiration_date.strftime("%Y-%m-%d"),
            'season': 'Spring 2018',
            'created_date': timezone.now().strftime("%Y-%m-%d"),
            'items': ['1']
        })

        self.assertEqual(Menu.objects.count(), 2)

    def test_edit_menu_view_get(self):
        """Test the rendering of the edit menu view"""
        resp = self.client.get(reverse('menu_edit',
                                       kwargs={'pk': self.menu.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/edit_menu.html')
        self.assertContains(resp, "Edit Menu")

    def test_edit_menu_view_post(self):
        """Test the posting of data from the edit menu view"""
        expiration_date = timezone.now() + timezone.timedelta(days=3)

        self.client.post(reverse('menu_edit', args=[self.menu.id]), {
            'expiration_date': expiration_date.strftime("%Y-%m-%d"),
            'season': 'Spring 2019',
            'created_date': timezone.now().strftime("%Y-%m-%d"),
            'items': ['1']
        })
        menu = Menu.objects.get(id=1)
        self.assertEqual(menu.season, 'Spring 2019')

    def test_edit_item_view_get(self):
        """Test the rendering of data from the item edit view"""
        resp = self.client.get(reverse('item_edit',
                                       kwargs={'pk': self.item.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_edit.html')
        self.assertContains(resp, "Edit Item")
