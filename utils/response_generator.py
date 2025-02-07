import time


def response_generator(response):
    for i in range(1, len(response)):
        yield response[:i]
        time.sleep(0.001)  # Adjust the speed as needed
