mask_const = -100
shaft_const = 127
busy_const = 120
target_const = 110

shafts = [
    (10, 60),
    (40, 30),
    (80, 80)
]

combines_shafts = [0, 2, 0]
combine_capacity = [4, 4, 3]
combine_speed = [20, 24, 22]
combines_max_speed = max(combine_speed)
combines_num = len(combines_shafts)

factory_performance = 40
warehouse1_capacity = 40
warehouse2_capacity = 20

combine_move_cost = [3, 3, 4]
salt_cost = 300
combiners_salary = 30
storing_cost = 1
days = 900
