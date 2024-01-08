from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)


    def test_recipe_home_view_returns_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)


    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')


    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('', response.content.decode('utf-8'))


    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # checking if this itens have in template
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)
        

    def test_recipe_home_template_not_loads_recipes_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn('', response.content.decode('utf-8'))


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

