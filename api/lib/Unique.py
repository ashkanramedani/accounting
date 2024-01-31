import uuid

namespace = uuid.UUID(int=True)
name = "H"


def unique(version: int = 1, mode: str = 'int'):
    if mode not in ['int', 'hex']:
        mode = 'hex'
    if version == 1:
        U = uuid.uuid1()
    elif version == 3:
        U = uuid.uuid3(namespace, name)
    elif version == 4:
        U = uuid.uuid4()
    else:
        U = uuid.uuid5(namespace, name)

    return U.int if mode == 'int' else U.hex


if __name__ == '__main__':
    print(unique(1))
    print(unique(3))
    print(unique(4))
    print(unique(5))

    print(unique(1, 'hex'))
    print(unique(3, 'hex'))
    print(unique(4, 'hex'))
    print(unique(5, 'hex'))
