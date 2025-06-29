import logging

def get_logger(name: str, level: str = "INFO"):
    """
    获取一个配置好的日志记录器。

    Args:
        name (str): 日志记录器的名称。
        level (str): 日志级别（例如："DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"）。

    Returns:
        logging.Logger: 配置好的日志记录器实例。
    """
    logger = logging.getLogger(name)
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logger.setLevel(numeric_level)

    # 避免重复添加处理器
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger 