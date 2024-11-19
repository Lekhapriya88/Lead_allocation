class Counsellor:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"Counsellor({attrs})"