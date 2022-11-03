def log_metrics(conf,metrics_df):
    '''Top-level decorator for grid-search evaluation
    
    :param conf: dictionary in function_parameter_name:list_of_values format
    :param metrics_df: constructed as shown in the examples
    
    '''
    import itertools
    from tqdm import tqdm

    keys = conf.keys()
    values = conf.values()
    values_cross = list(itertools.product(*list(values)))
    
    def _decorate(input_fn):
        def wrapper(*args, **kwargs):
          with tqdm(total=len(values_cross)) as pbar:
            for _value_list in values_cross:
              input_args = dict(zip(keys, _value_list))
              pbar.set_description(str(input_args))
              
              metrics = input_fn(*args, **kwargs, **input_args)
              
              if metrics: # fail-safe for when the above funciton has no return               
                pbar.write(str(input_args) + ' ' + str(metrics))
                metrics_df.loc[_value_list, list(metrics.keys())] = list(metrics.values())
                
              pbar.update(1)

        return wrapper
    return _decorate