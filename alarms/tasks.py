from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BroadcastAlarm
import json
from celery import Celery, states
from celery.exceptions import Ignore
import asyncio

@shared_task(bind = True)
def broadcast_alarm(self, data):
    print(data)
    try:
        alarm = BroadcastAlarm.objects.filter(id = int(data))
        if len(alarm)>0:
            alarm = alarm.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "alarm_broadcast",
                {
                    'type': 'send_alarm',
                    'message': json.dumps(alarm.message),
                }))
            alarm.sent = True
            alarm.save()
            return 'Done'

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except:
        self.update_state(
                state = 'FAILURE',
                meta = {
                        'exe': "Failed"
                        # 'exc_type': type(ex).__name__,
                        # 'exc_message': traceback.format_exc().split('\n')
                        # 'custom': '...'
                    }
            )

        raise Ignore()