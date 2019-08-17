from example.utils.utils import sayAnything, sayHello

information = {
    "name": "Mokke",
    "greeting": "Nice to meet you!"
}


def Introduction(information):
    sayHello()
    intro = "My name is " + information['name']
    sayAnything(intro)
    sayAnything(information['greeting'])


if __name__ == '__main__':
    Introduction(information)

