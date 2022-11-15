def datefixer(dateconf):
    '''Fixes date-columns in pyspark dataframes
    
    :param dateconf:  dictionary of column-format mappings
    
    '''
    import functools
    import pyspark
    from pyspark.sql import functions as F
    def _datefixer(func):

        @functools.wraps(func)
        def wrapper(df, *args, **kwargs):
            df_dateconf = {}
            for key, values in dateconf.items():
                df_dateconf[key] = [i for i in df.columns if i in values]


            for dateformat in df_dateconf.keys():
                for datecolumn in df_dateconf[dateformat]:
                    if dateformat == 'american':
                        df = df.withColumn(datecolumn, F.to_date(datecolumn, 'dd/MM/yyyy'))
                    if dateformat == 'julian':
                        df = df.withColumn(datecolumn, F.to_date(datecolumn, 'yyyy/DDD'))
                    if dateformat == 'inversejulian':
                        df = df.withColumn(datecolumn, F.to_date(datecolumn, 'DDD/yyyy'))
            return func(df, *args, **kwargs)

        return wrapper

    return _datefixer
