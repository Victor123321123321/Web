class MyDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, item):
        return self.get(item, None)

test_obj = MyDict(username='USER1', password='PASS', location='Moscow')
print(test_obj.username)
print(test_obj['password'])
print(test_obj.address)
print(test_obj)