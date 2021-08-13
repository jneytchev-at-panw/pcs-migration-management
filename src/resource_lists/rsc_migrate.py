def migrate(tenant_sessions: list):
    '''
    Accepts a list of tenant session objects.
    
    Migrates all resource lists from the first tenant, (source tenant)
    to all other tenants (clone tenants).
    '''