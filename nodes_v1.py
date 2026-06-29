# Random Seed Batch Generator — V1 format

import random


class RandomSeedBatchGenerator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "initial_seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "control_after_generate": "randomize",
                    "tooltip": "Starting seed for reproducible randomization. The actual group seeds are derived from this value."
                }),
                "step": ("INT", {
                    "default": 1,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "tooltip": "Step between seeds within a single group. Set to 0 for all seeds in a group to be equal."
                }),
                "count": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 0xffffffffffffffff,
                    "tooltip": "Number of seeds per group."
                }),
                "groups": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 0xffffffffffffffff,
                    "tooltip": "Number of groups to generate. Each group starts from a random seed."
                }),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seeds",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "seed_batch"
    CATEGORY = "seed_batch_generator"
    DESCRIPTION = """
Generate multiple groups of seeds for batch image processing.
Each group produces similar variations by incrementing seeds with a fixed step.
Use multiple groups to run several independent variation sets in a single execution.
step — step between seeds within a group (0 = all seeds in group are equal).
count — number of seeds per group.
groups — number of groups to generate.
initial_seed — starting seed for reproducible randomization. When set, the same initial_seed + control_after_generate will produce the same sequence of seeds.
control_after_generate — controls how initial_seed changes after each execution: fixed, increment, decrement, or randomize.
"""

    def seed_batch(self, step, count, groups, initial_seed):
        seeds = []
        mask = 0xffffffffffffffff
        max_start = mask - step - count + 1
        if max_start < 0:
            return (seeds,)
        rng = random.Random(initial_seed)
        for _ in range(groups):
            start = rng.randint(0, max_start)
            for i in range(count):
                seeds.append(start + step + i)
        return (seeds,)


NODE_CLASS_MAPPINGS = {
    "Random Seed Batch Generator": RandomSeedBatchGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Random Seed Batch Generator": "Random Seed Batch Generator",
}
