"""
WebUI 组件模块

包含各种 UI 组件的实现
"""

from .basic_tab import create_basic_tab
from .query_tab import create_query_tab
from .analysis_tab import create_analysis_tab
from .resource_monitor_tab import create_resource_monitor_tab
from .module_overview_tab import create_module_overview_tab

__all__ = [
    "create_basic_tab",
    "create_query_tab", 
    "create_analysis_tab",
    "create_resource_monitor_tab",
    "create_module_overview_tab"
] 