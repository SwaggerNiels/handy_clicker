import re
from pprint import pprint

def slice_parser():

    def func(my_string : str):
        if not my_string.__contains__(':'):
            return(int(my_string))
        return slice(*map(lambda x: int(x.strip()) if x.strip() else None, my_string.split(':'))) 
    
    return func

file_paths = ['P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03465.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03466.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03467.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03460.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03468.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03469.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03470.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03471.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03472.csv', 'P:\\Mitutoyo\\Meetrapporten\\Frencken Mechatronics\\90050163 Pre Mounted Lateral Carriage 00437-00-144\\2023\\IM DATA\\00437-00-143     volgnr-SAM 23-45-437-03473.csv']
index_pairs =[(151, 155), (151, 155), (151, 155), (151, 155), (151, 155), (151, 155), (151, 155), (151, 155), (151, 155), (151, 155)]

file_paths = file_paths[:2]
index_pairs = index_pairs[:2]

variable_program = {}
variable_program['path_pre_id'] = []
variable_program['i'] = []
variable_program['path_post_id'] = []

action = []
action.append('')
action.append('<path_pre_id><i><path_post_id>')

for path, inds in zip(file_paths,index_pairs):
    parameter = path[inds[0]:inds[1]]
    variable_program['path_pre_id'].append(path[:inds[0]])
    variable_program['i'].append(parameter)
    variable_program['path_post_id'].append(path[inds[1]:])

# print(list(variable_program.items()))
parameter_sets = [[(key,parameter[i]) 
                  for key,parameter in variable_program.items()]
                  for i             in range(len(list(variable_program.items())[0][1]))]
pprint(parameter_sets)
# quit()

def action_set_parameter(action, variable_name, parameter, parameter_index,parameter_indices):
    variable_replace=[(variable_name,parameter)] # the replace list of the variable
                                                
    if variable_replace != None: # if variable is typing variable this will be done
        for adaption in variable_replace: #Do an adaption to the original typing-action
            # adaption = ('old_substring', 'new_substring')
            old_s,new_s = adaption
            if parameter_index != None:
                sp = slice_parser()
                # print('action: ', action)
                # print("var_pattern: ", var_pattern)
                # print("find?: ", re.findall(var_pattern, action))
                var_pattern = old_s
                # print('var_pattern: ', var_pattern)
                # print('action: ', action)
                if re.search(var_pattern, action) == None:
                    continue
                else:
                    # print('found: ',re.search(var_pattern, action)[0])

                    indexed_var_pattern = old_s + r'\[([0-9\:]*)\]'
                    if re.search(indexed_var_pattern, action) != None:
                        slice_str = re.findall(indexed_var_pattern, action)[0]
                        indices = parameter_indices[sp(slice_str)]
                        if not hasattr(indices, '__iter__'):
                            indices = [indices]
                        # print(parameter_index, ' in? ', indices)
                        if parameter_index not in indices:
                            continue
                        old_s = '<' + re.search(indexed_var_pattern, action)[0] + '>'
                        action = action.replace(old_s,new_s)
                        continue

                    old_s = '<' + re.search(var_pattern, action)[0] + '>'
                    action = action.replace(old_s,new_s)
                    continue

    return(action)

parameter_indices = list(range(len(parameter_sets)))
for parameter_index,parameter_set in enumerate(parameter_sets): # for each parameter witin the variable adapt (if within optional slice)
    adapted_action = action[1]
    pprint('___________'+str(parameter_index))
    for var,par in parameter_set:
        pprint('___________'+var)
        adapted_action = action_set_parameter(adapted_action,
                                              var,
                                              par,
                                              parameter_index,
                                              parameter_indices,)
        print('ADAPTED ACTION: ', adapted_action)