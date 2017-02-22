from cloudfoundry_client.entities import EntityManager


class StackManager(EntityManager):
    def __init__(self, target_endpoint, client):
        super(StackManager, self).__init__(target_endpoint, client, '/v2/stacks')

    def update(self, stack_guid, parameters):
        return super(StackManager, self)._update(stack_guid, parameters)
