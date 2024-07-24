# two sum

# def ts(nums, target):
#     d = {}
#     for i in range(len(nums)):
#         if target - nums[i] in d:
#             return [d[target - nums[i]], i]
#         d[nums[i]] = i
#
#
# print(ts([2, 7, 8, 6], 9))

from datetime import datetime, timedelta

start = datetime.now()
# print(f'START {start}')
# for i in range(1000000):
#     print(i)
# print(f'START {start} TYPE {type(start)}')
# finish = datetime.now() - start
# print(f'FINISH {finish} TYPE {type(finish)}')
print(start)
print(start.strftime('%d %B %Y'))
format_of_time = start.strftime("%H:%M")

print(format_of_time)


clock_in_half_hour = datetime.now() + timedelta(hours=12)
print(clock_in_half_hour.strftime('%d %B %Y'))
print(clock_in_half_hour.strftime('%H:%M'))
