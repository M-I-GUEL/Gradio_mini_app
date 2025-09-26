import os
from datetime import datetime
import csv
#COMMAND LINE STOPWATCH WITH LAP TRACKING(intermediate)
commands_list = ['start','lap','reset','quit','stop','resume','pause']
command = input('Command: (start/lap/pause/resume/stop/reset/quit): ')
command = command.strip().lower()
if command not in commands_list:
    command = input('please enter a valid command (start/lap/pause/resume/stop/reset/quit):')
state = 'idle'
laps = []
last_lap = None
start_time=None
paused_time = 0
paused_start= None
def com_mand():
    command = input('Command: ')
    command = command.strip().lower()
    if command not in commands_list:
        command = input('please enter a valid command (start/lap/pause/resume/stop/reset/quit):')
    return command
def total_second(total_seconds):
    hour = (int(total_seconds)//3600)
    minute = (int(total_seconds)%3600)//60
    seconds = (int(total_seconds)%60)
    centiseconds = round((total_seconds-int(total_seconds))*100)
    if centiseconds==100:
        centiseconds = 0
        seconds+=1
        if seconds == 60:
            seconds = 0
            minute+=1
            if minute==60:
                minute = 0
                hour+=1
    if hour<10:
        hour = f'0{hour}'
    if minute<10:
        minute = f'0{minute}'
    if seconds<10:
        seconds = f'0{seconds}'
    if centiseconds<10:
        centiseconds = f'0{centiseconds}'
    return f'{hour}:{minute}:{seconds}.{centiseconds}'
while True:
    if command=='start':
        if state == 'idle':
            start_time = datetime.now()
            laps = []
            last_lap = datetime.now()
            paused_time = 0
            state = 'running'
            print(f'Started at {start_time.strftime('%H:%M:%S')}')
        else:
            print('Already started!')
        command = com_mand()
    elif command=='lap':
        if state=='running':
            current_time = datetime.now()
            lap_duration = current_time-last_lap
            lap_duration = lap_duration.total_seconds()
            total_elapsed = current_time-start_time
            total_elapsed = total_elapsed.total_seconds()
            last_lap = current_time
            laps.append(lap_duration)
            number = len(laps)
            print(f'Lap {number} - {total_second(lap_duration)} (Total: {total_second(total_elapsed)})')
        elif state=='idle':
            print('Stopwatch not started yet...')
        else:
            print('Stopwatch is paused! cannot record lap')
        command = com_mand()
    elif command=='pause':
        if state=='running':
            paused_start = datetime.now()
            total_elapsed = paused_start-start_time
            total_elapsed = total_elapsed.total_seconds()
            state = 'paused'
            print(f'Paused at {total_second(total_elapsed)}')
        elif state=='idle':
            print('Stopwatch not started yet... ')
        else:
            print('Stopwatch is already paused!')
        command = com_mand()
    elif command=='resume':
        if state =='paused':
            current_time = datetime.now()
            paused_duration = current_time-paused_start
            paused_duration = paused_duration.total_seconds()
            paused_time = paused_duration+paused_time
            state = 'running'
            print('Resumed')
        elif state == 'running':
            print('Stopwatch already running!')
        else:
            print('Stopwatch not started yet... ')
        command = com_mand()
    elif command=='stop':
        if state =='running':
            current_time = datetime.now()
            final_time_elapsed = (current_time-start_time).total_seconds()-paused_time
            state = 'idle'
        elif state =='paused':
            final_time_elapsed = (paused_start-start_time).total_seconds()-paused_time
            state = 'idle'
        else:
            print("Stopwatch hasn't started yet...")
        if len(laps)>0:
            min_laps = total_second(min(laps))
            max_laps = total_second(max(laps))
            average_laps = total_second(sum(laps)/len(laps))
        
            print(f'''Summary
-------
Total time = {total_second(final_time_elapsed)}
Laps = {len(laps)}
Fastest lap = {min_laps} (Lap {laps.index(min(laps))+1})
Slowest lap = {max_laps} (Lap {laps.index(max(laps))+1})
average lap = {average_laps}
''')
        else:
            print(f'''Summary
                        -------
Total time = {total_second(final_time_elapsed)}
Laps = {len(laps)}
Fastest lap = no lap recorded
Slowest lap = no lap recorded
average lap = no lap recorded
''')    
        date = datetime.now()
        date = date.strftime('%Y:%m:%d')
        if len(laps)>0:
            final_time_elapsed_str = total_second(final_time_elapsed)
            start_time_str = start_time.strftime('%H:%M:%S')
            min_laps = total_second(min(laps))
            max_laps = total_second(max(laps))
            average_laps = total_second(sum(laps)/len(laps))
        else:
            start_time_str = '00:00:00.00'
            min_laps = '00:00:00.00'
            max_laps = '00:00:00.00'
            average_laps= '00:00:00.00'
            final_time_elapsed_str = '00:00:00.00'
        if os.path.exists('stopwatch_sessions.csv'):
            if os.path.getsize('stopwatch_sessions.csv')==0:
                with open('stopwatch_sessions.csv', 'a') as file:
                    file_content = csv.writer(file)
                    file_content.writerow(['Date', 'Start_time', 'Total_duration', 'Laps','Fastest', 'Slowest', 'Average'])
                    file_content.writerow([date, start_time_str, final_time_elapsed_str, len(laps), min_laps, max_laps, average_laps])
            else:
                with open('stopwatch_sessions.csv', 'a') as file:
                    file_content = csv.writer(file)
                    file_content.writerow([date, start_time_str, final_time_elapsed_str, len(laps), min_laps, max_laps, average_laps])
        else:
            with open('stopwatch_sessions.csv', 'a'):
                pass
        command = com_mand()
    elif command=='reset':
        state = 'idle'
        laps.clear()
        last_lap = None
        start_time = None
        paused_start = None
        paused_time = 0
        print('Stopwatch reset successfully!')
        command = com_mand()
    elif command=='quit':
        break
print('Session ended')
