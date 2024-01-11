from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)


    def test_recipe_category_view_returns_not_found_whitout_recipe(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    
    def test_recipe_category_template_loads_recipes(self):
        title_test = 'Category Test'
        self.make_recipe(title=title_test)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(title_test, content)


    def test_recipe_category_template_not_loads_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:category', kwargs={'category_id':recipe.category.id}))
        self.assertEqual(response.status_code, 404)

