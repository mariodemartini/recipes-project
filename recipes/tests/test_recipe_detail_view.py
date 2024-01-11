from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:details', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    
    def test_recipe_detail_view_returns_not_found_whitout_recipe(self):
        response = self.client.get(reverse('recipes:details', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    
    def test_recipe_detail_template_loads_one_recipe(self):
        detail_test = 'Detail Page Test'
        self.make_recipe(title=detail_test)

        response = self.client.get(reverse('recipes:details', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(detail_test, content)

    
    def test_recipe_detail_template_not_loads_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:details', kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)

