def ingredients_to_txt(ingredients):
    shopping_list = ''
    for ingredient in ingredients:
        shopping_list += (
            f"{ingredient['ingredient__name']} "
            f"({ingredient['ingredient__measurement_unit']}) - "
            f"{ingredient['sum']}\n"
        )
    return shopping_list
