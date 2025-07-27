from tests.test_api import test_post_get
from tests.test_notifier import post_close_to_five_minutes_test

if __name__ == "__main__":
    print("Testing API:")
    test_post_get()
    print("\n \n \n")
    print("Testing notifier:")
    post_close_to_five_minutes_test()