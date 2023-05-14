from mobile.mobile_test_for_rg.page_objects.page_objects import RG_Android
from mobile.mobile_test_for_rg.conftest import PRODUCT_NAME


def test_product_rating(emulated_device):
    """
    Tests if rating of a chosen product's (PRODUCT_NAME is defined in conftest.py) rating is more than 4
    :param device: fixture of a device
    :return: asserts if product's rating > 4
    """
    rg = RG_Android(emulated_device)
    rg.open_search()
    rg.find_product(PRODUCT_NAME)
    rating = rg.get_product_rating()
    print("Rating of product '{0}' is: {1}".format(PRODUCT_NAME, rating))
    assert float(rating) > 4
