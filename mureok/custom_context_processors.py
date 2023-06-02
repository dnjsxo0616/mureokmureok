from alarms.models import BroadcastAlarm
def alarms(request):
    allalarms = BroadcastAlarm.objects.all()
    return {'alarms': allalarms}