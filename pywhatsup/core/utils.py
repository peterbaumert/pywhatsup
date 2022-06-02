class Utils:
    def _parse_values(par, values, default_ret):
        def list_parser(key_name, list_item):
            if isinstance(list_item, dict):
                lookup = getattr(par.__class__, key_name, None)
                if not isinstance(lookup, list):
                    return default_ret(list_item)
                else:
                    model = lookup[0]
                    return model(list_item)
            return list_item

        for k, v in values.items():
            if isinstance(v, dict):
                lookup = getattr(par.__class__, k, None)
                if lookup:
                    v = lookup(v)
                else:
                    v = default_ret(v)

            elif isinstance(v, list):
                v = [list_parser(k, i) for i in v]

            setattr(par, k, v)
