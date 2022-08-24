from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.TextField(
        'Название',
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        help_text='Введите единицу измерения',
        max_length=10
    )


    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.TextField(
        'Название',
        help_text='Введите название тэга'
    )
    color = models.CharField(max_length=7, default='#ffffff')
    slug = models.SlugField(
        'Slug',
        help_text='Введите slug'
    )


    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор рецепта записывается автоматически'
    )
    name = models.TextField(
        'Название',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        help_text='Выберите картинку'
    )
    text = models.TextField(
        'Описание',
        help_text='Введите описание рецепта'
    )
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Введите время приготовления в минутах',
        db_index=True,
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True,
        help_text='Дата публикации формируется автоматически',
        db_index=True,
    )


    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
    

    def __str__(self):
        return self.text[:15]


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.IntegerField(
        'Количество',
        help_text='Введите количество'
    )


    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='unique follow'
            )
        ]


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Тэг рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'], name='unique follow'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Задаётся автоматически аутентифицированный пользователь.'
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт добавленный в избранное',
        help_text='Задаётся рецепт который добавили в избранное'
    )


    class Meta:
        verbose_name = 'Рецепт в избранном пользователя'
        verbose_name_plural = 'Рецепты в избранном пользователя'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite_recipe'], name='unique follow'
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Задаётся автоматически аутентифицированный пользователь.'
    )
    added_to_cart_recipe = models.ForeignKey(
        Recipe,
        related_name='added_to_cart_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт добавленный в корзину',
        help_text='Задаётся рецепт который добавили в корзину'
    )


    class Meta:
        verbose_name = 'Рецепт в корзине пользователя'
        verbose_name_plural = 'Рецепты в корзине пользователя'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'added_to_cart_recipe'], name='unique follow'
            )
        ]
