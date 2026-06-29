try:
    from .nodes_v3 import comfy_entrypoint
    __all__ = ["comfy_entrypoint"]
except ImportError:
    from .nodes_v1 import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    __all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
