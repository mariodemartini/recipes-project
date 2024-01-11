from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_load_correct_view_function(self):
        url = resolve(reverse('recipes:search'))
        self.assertIs(url.func, views.search)

    
    def test_recipe_search_load_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?search=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')


    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search')) 
        self.assertEqual(response.status_code, 404)

    
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?search=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            '&quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )