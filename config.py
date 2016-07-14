class Config(object):
    with open('secret_key', 'r') as f:
        secret_key = f.read()
    staging_env_path = '/Users/balsamo/test_staging_env'
