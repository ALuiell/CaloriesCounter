from app.services.parser import parse_food_message


def test_parse_one_item():
    items = parse_food_message("гречка 120")
    assert len(items) == 1
    assert items[0].product_text == "гречка"
    assert items[0].weight_g == 120


def test_parse_with_commas_and_newlines():
    items = parse_food_message("гречка 120, курица 180\nпомидор 80")
    assert [item.product_text for item in items] == ["гречка", "курица", "помидор"]


def test_parse_ignores_empty_fragments():
    items = parse_food_message("гречка 120,,\n\nкурица 180")
    assert len(items) == 2


def test_parse_unrecognized_without_weight():
    items = parse_food_message("домашний пирог кусок")
    assert items[0].product_text == ""
    assert items[0].weight_g == 0


def test_parse_removes_gram_tokens():
    items = parse_food_message("гречка 120 г, рис 80 грамм")
    assert [item.product_text for item in items] == ["гречка", "рис"]
