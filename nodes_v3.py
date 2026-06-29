# Random Seed Batch Generator — V3 format

import random
from comfy_api.latest import ComfyExtension, io
from comfy_api.latest._io import ControlAfterGenerate


class RandomSeedBatchGenerator(io.ComfyNode):
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

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="RandomSeedBatchGenerator",
            display_name="Random Seed Batch Generator",
            category="seed_batch_generator",
            inputs=[
                io.Int.Input(
                    "initial_seed",
                    default=0,
                    min=0,
                    max=0xffffffffffffffff,
                    control_after_generate=ControlAfterGenerate.randomize,
                    tooltip="Starting seed for reproducible randomization. The actual group seeds are derived from this value.",
                ),
                io.Int.Input(
                    "step",
                    default=1,
                    min=0,
                    max=0xffffffffffffffff,
                    tooltip="Step between seeds within a single group. Set to 0 for all seeds in a group to be equal.",
                ),
                io.Int.Input(
                    "count",
                    default=1,
                    min=1,
                    tooltip="Number of seeds per group.",
                ),
                io.Int.Input(
                    "groups",
                    default=1,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Number of groups to generate. Each group starts from a random seed.",
                ),
            ],
            outputs=[
                io.Int.Output("seeds", is_output_list=True),
            ],
        )

    @classmethod
    def execute(cls, step, count, groups, initial_seed):
        seeds = []
        mask = 0xffffffffffffffff
        max_start = mask - step - count + 1
        if max_start < 0:
            return io.NodeOutput(seeds)
        rng = random.Random(initial_seed)
        for _ in range(groups):
            start = rng.randint(0, max_start)
            for i in range(count):
                seeds.append(start + step + i)
        return io.NodeOutput(seeds)


class Extension(ComfyExtension):
    async def get_node_list(self):
        return [RandomSeedBatchGenerator]


async def comfy_entrypoint() -> ComfyExtension:
    return Extension()
