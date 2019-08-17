def add_parameters(request, **kwargs):
    path = request.get_full_path().split('?')
    new_path = path[0]
    current_parameters = {}
    if '?' in path:
        symbol = '&'
        temp_parameters = path[1]
        for par in temp_parameters.split('&'):
            tmp = par.split('=')
            current_parameters[tmp[0]] = tmp[1]
    else:
        symbol = '?'
    new_path += symbol
    for key, value in kwargs.items():
        current_parameters[key] = value
    for key, value in current_parameters.items():
        new_path += f'{key}={value}&'
    new_path = new_path[:-1]
    return new_path
