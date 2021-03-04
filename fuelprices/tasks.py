from fuelapp.celery import app
from fuelprices.models import Omc


@app.task(bind=True)
def test_object_task(self):
    o = Omc.objects.last()
    Omc.objects.create(name=str(o.id + 1))
    print(o)
    return 0
