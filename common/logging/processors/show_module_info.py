from structlog._frames import _find_first_app_frame_and_name


class ShowModuleInfo(object):
    def __call__(self, logger, method_name, event_dict):
        f, name = _find_first_app_frame_and_name([
            "logging",
            __name__,
        ])

        event_dict['_trace_code'] = '{}:{}:{}'.format(
            f.f_code.co_filename,
            f.f_code.co_name,
            f.f_lineno,
        )

        return event_dict
