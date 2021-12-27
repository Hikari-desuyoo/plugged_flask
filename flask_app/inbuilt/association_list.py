class AssociationList:
    def __init__(self, name, id_list, model_class, belonger):
        self.id_list = id_list
        self.model_class = model_class
        self.belonger = belonger
        self.name = name

    def __contains__(self, key):
        assert isinstance(key, self.model_class)
        return key['_id'] in self.id_list

    def is_empty(self):
        return len(self.id_list) == 0

    def fetch_all(self):
        return [
            self.fetch_by_document_id(document_id)\
            for document_id in self.id_list
            ]

    def fetch_by_index(self, index):
        return self.model_class.find_by(_id=self.id_list[index])

    def fetch_by_document_id(self, document_id):
        return self.model_class.find_by(_id=document_id)

    def add(self, model_instance):
        self.id_list.append(model_instance['_id'])
        self.belonger[self.name] = self.as_raw()

    def remove(self, model_instance):
        self.id_list.remove(model_instance['_id'])
        self.belonger[self.name] = self.as_raw()

    def as_raw(self):
        return sorted(self.id_list)