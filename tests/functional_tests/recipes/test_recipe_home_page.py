from unittest.mock import patch
import pytest
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_whitout_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)
        

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        # User opens the page
        self.browser.get(self.live_server_url)

        # You see a search field with the text "Pesquise a receita aqui"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Pesquise a receita aqui..."]'
        )

        # Click on this input and type the search term
        # to find the recipe the desired title
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # The user sees what they were looking for on the page
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

        