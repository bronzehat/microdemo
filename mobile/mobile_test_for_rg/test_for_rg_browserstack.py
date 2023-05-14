"""
This test is an experiment with Rate&Goods testing in BrowserStack.
It checks profile id and build version.
"""
from mobile.mobile_test_for_rg.page_objects.page_objects import RG_Android


def test_rg_browserstack(browserstack_device):
    rg = RG_Android(browserstack_device)
    rg.open_settings()
    id = rg.profile_id()
    build = rg.build_version()
    print("\nProfile ID is: {}, Build version is: {}".format(id, build))
    assert id and build
