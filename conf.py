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
combine_capacity = [5, 6, 3]
combine_speed = [10, 40, 20]
combines_max_speed = max(combine_speed)
combines_num = len(combines_shafts)

factory_performance = 20
warehouse1_capacity = 40
warehouse2_capacity = 20000

combine_move_cost = [40, 20, 30]
salt_cost = 300
storing_cost = 10
days = 1000
