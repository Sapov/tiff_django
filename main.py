class GenericView:
    def __init__(self, methods=('GET',)):
        self.methods = methods
        if methods == ('PUT', 'POST',):
            self.methods = ('PUT', 'POST',)

    def get(self, request):
        return ""

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


class DetailView(GenericView):
    def render_request(self, request, method):
        if method in self.methods:
            if 'url' in request:
                return getattr(self, method.lower())(request)
            else:
                raise TypeError('request не содержит обязательного ключа url')
        else:
            raise TypeError('данный запрос не может быть выполнен')


# dv = DetailView()  # по умолчанию methods=('GET',)
# dv = DetailView(methods=('PUT', 'POST'))
dv = DetailView()
html = dv.render_request({'url': 'https://site.ru/home'}, 'GET')  # url: https://site.ru/home
print(dir(dv))
print(dv.__dict__)
