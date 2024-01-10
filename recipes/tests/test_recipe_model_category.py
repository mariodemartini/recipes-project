from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()


    def test_recipe_category_model_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )


    def test_recipe_category_model_name_have_more_50_chars(self):
        self.category.name = 'A' * 51
        with self.assertRaises(ValidationError):
            self.category.full_clean()