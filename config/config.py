import yaml

with open(r"config\config.yaml", 'r', encoding='utf-8') as f:
    conf = yaml.safe_load(f)
    conn_string = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(**conf)
