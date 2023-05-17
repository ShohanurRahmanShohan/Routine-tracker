from flask import Flask, render_template
import datetime
import time
from routine import routine

app = Flask(__name__)

def get_current_activity():
    current_day = datetime.datetime.now().strftime("%A")
    current_time = datetime.datetime.now().time()

    if current_day in routine:
        day_routine = routine[current_day]
        for activity, time_slot in day_routine.items():
            start_time, end_time = time_slot.split(' - ')
            start_datetime = datetime.datetime.strptime(start_time, "%I:%M %p").time()
            end_datetime = datetime.datetime.strptime(end_time, "%I:%M %p").time()
            if start_datetime <= current_time <= end_datetime:
                return activity, end_datetime

    return "No scheduled activity at the moment.", None

@app.route('/')
def home():
    current_activity, end_time = get_current_activity()
    if end_time:
        remaining_time = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.now()
        remaining_minutes = remaining_time.seconds // 60
        remaining_seconds = remaining_time.seconds % 60
        remaining_time_formatted = f"{remaining_minutes:02d}:{remaining_seconds:02d}"
        day_routine = routine[datetime.datetime.now().strftime("%A")]
        return render_template('index.html', activity=current_activity, remaining_time=remaining_time_formatted, routine=day_routine)
    else:
        return render_template('index.html', activity=current_activity)

if __name__ == '__main__':
    app.run(debug=True)
