class ProfileTypeConverter:
    regex = 'business|customer'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
