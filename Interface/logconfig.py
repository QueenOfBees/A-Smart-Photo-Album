import logging, os


class Logging:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_ins"):
            cls._ins = super().__new__(cls)
        return cls._ins

    def __call__(self):
        log_dir = os.environ.get("Log")
        if not log_dir:
            log_dir = "D:\\Log4py"
            if not os.path.exists("D:\\Log4py"):
                os.mkdir("D:\\Log4py")
                with open(os.path.join("D:\\Log4py", "misc.log"), "w") as f:
                    f.close()
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(filename=os.path.join(log_dir, "misc.log"), level=logging.DEBUG, format=LOG_FORMAT,
                            datefmt=DATE_FORMAT)


config = Logging()
