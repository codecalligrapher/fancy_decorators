"""This decorator takes an arbitrary config with parameters,
e.g.
  conf = {
    'over': [0.1, 0.5], 
    'under': [0.2, 0.5]
  }
 
 There is no restriction on the number of keys the above has, it will calculate a cross
 product of all the options

 AND a metrics_df created as follows:
 conf = {
    # your grid-search params
  }
  
  # this allows ease of indexing
  values = conf.values()
  keys = conf.keys()
  midx =  MultiIndex.from_product(list(values), names=list(keys))
  metrics_df = DataFrame(index=midx)
  
  #HOW TO USE:
  Decorate your funciton
  @log_metrics(conf, metrics_df)
  def evaluate_sampling(X_train, y_train, X_test, y_test, over, under):
    ...
    return dict() <- this MUST be a dictionary of metrics:metric_value
 
"""

def log_metrics(conf,metrics_df):
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