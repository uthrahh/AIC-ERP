def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['equipment'].queryset = Equipment.objects.filter(
        active=True
    )