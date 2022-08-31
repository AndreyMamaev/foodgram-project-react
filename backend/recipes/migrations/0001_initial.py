# Generated by Django 4.1 on 2022-08-31 07:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('name', models.TextField(
                    help_text='Введите название ингридиента',
                    verbose_name='Название'
                )),
                ('measurement_unit', models.CharField(
                    help_text='Введите единицу измерения',
                    max_length=10, verbose_name='Единицы измерения'
                )),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('amount', models.PositiveSmallIntegerField(
                    help_text='Введите количество',
                    verbose_name='Количество'
                )),
                ('ingredient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='recipes.ingredient'
                )),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('name', models.TextField(
                    help_text='Введите название рецепта',
                    verbose_name='Название'
                )),
                ('image', models.ImageField(
                    help_text='Выберите картинку',
                    upload_to='recipes/images/', verbose_name='Картинка'
                )),
                ('text', models.TextField(
                    help_text='Введите описание рецепта',
                    verbose_name='Описание'
                )),
                ('cooking_time', models.PositiveSmallIntegerField(
                    db_index=True,
                    help_text='Введите время приготовления в минутах',
                    verbose_name='Время приготовления'
                )),
                ('pub_date', models.DateTimeField(
                    auto_now_add=True, db_index=True,
                    help_text='Дата публикации формируется автоматически',
                    verbose_name='Дата публикации'
                )),
                ('author', models.ForeignKey(
                    help_text='Автор рецепта записывается автоматически',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recipes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор рецепта'
                )),
                ('ingredients', models.ManyToManyField(
                    through='recipes.IngredientRecipe',
                    to='recipes.ingredient'
                )),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('name', models.TextField(
                    help_text='Введите название тэга',
                    verbose_name='Название'
                )),
                ('color', models.CharField(
                    default='#ffffff', max_length=7
                )),
                ('slug', models.SlugField(
                    help_text='Введите slug', verbose_name='Slug'
                )),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('recipe', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='recipes.recipe'
                )),
                ('tag', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='recipes.tag'
                )),
            ],
            options={
                'verbose_name': 'Тэг рецепта',
                'verbose_name_plural': 'Теги рецепта',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                through='recipes.TagRecipe', to='recipes.tag'
            ),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='recipe_ingredients', to='recipes.recipe'
            ),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('favorite_recipe', models.ForeignKey(
                    help_text='Задаётся рецепт который добавили в избранное',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorite_recipe', to='recipes.recipe',
                    verbose_name='Рецепт добавленный в избранное'
                )),
                ('user', models.ForeignKey(
                    help_text='Задаётся автоматически '
                    'аутентифицированный пользователь.',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorites',
                    to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'
                )),
            ],
            options={
                'verbose_name': 'Рецепт в избранном пользователя',
                'verbose_name_plural': 'Рецепты в избранном пользователя',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('added_to_cart_recipe', models.ForeignKey(
                    help_text='Задаётся рецепт который добавили в корзину',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='added_to_cart_recipe',
                    to='recipes.recipe',
                    verbose_name='Рецепт добавленный в корзину'
                )),
                ('user', models.ForeignKey(
                    help_text='Задаётся автоматически '
                    'аутентифицированный пользователь.',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='cart',
                    to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'
                )),
            ],
            options={
                'verbose_name': 'Рецепт в корзине пользователя',
                'verbose_name_plural': 'Рецепты в корзине пользователя',
            },
        ),
        migrations.AddConstraint(
            model_name='tagrecipe',
            constraint=models.UniqueConstraint(
                fields=('tag', 'recipe'), name='unique tag'
            ),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(
                fields=('ingredient', 'recipe'), name='unique ingredient'
            ),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(
                fields=('user', 'favorite_recipe'), name='unique favorite'
            ),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(
                fields=('user', 'added_to_cart_recipe'), name='unique cart'
            ),
        ),
    ]