from metadataclient.v1.client import Client


def metadataclient():
    endpoint = 'http://localhost:5000'
    insecure = False
    token_id = '12casc2'

    return Client(endpoint=endpoint, token=token_id, insecure=insecure)


def main():
    # metadataclient().metadata_client.get_ui_data()
    metadataclient().metadata_client.get_conductor_data()
    admin = metadataclient().metadata_admin
    # print admin.list_ui()
    # print admin.list_ui('Murano')
    # print admin.list_agent()
    # workflows =  admin.list_workflows()
    # for key, value in workflows.iteritems():
    #     for i in value:
    #         print i
    # heat = metadataclient().metadata_admin.list_heat()
    # for key, value in heat.iteritems():
    #     for i in value:
    #         print i

    # admin.get_file('ui', 'WebServer.yaml')
    # print admin.get_file('ui', 'Murano/Demo.yaml')
    # admin.create_directory('ui', 'test')
    # admin.delete_dir('ui', 'Murano/README.rst')

if __name__ == "__main__":
    main()
