birds = {}
while True:
    bird = input('Введите птичку: ')  # Goldfinch: 10
    if bird == '':
        break
    name, count = bird.split(':')
    birds[name] = birds.get(name, 0) + int(count)

print(birds)
